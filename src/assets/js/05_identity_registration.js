(() => {
    const IDENTITY_REGISTER_URL = '/api/identity/register-current-user';
    const USER_SESSION_TOUCH_URL = '/api/user-session/touch';

    const PAGE_LOADER_READY_EVENT = 'ada:page-loader-ready';

    const IDENTITY_REGISTER_DELAY_MS = 600;
    const FALLBACK_DELAY_MS = 2500;
    // const HEARTBEAT_MS = 5 * 60 * 1000;
    const HEARTBEAT_MS = 60 * 1000;
    const STORAGE_NAMESPACE = 'ada:user-session:v1';

    const STORAGE_KEYS = {
        identityChecked: `${STORAGE_NAMESPACE}:identity-checked`,
        clientSessionId: `${STORAGE_NAMESPACE}:client-session-id`,
        sessionRegistered: `${STORAGE_NAMESPACE}:session-registered`,
        lastVisibilityState: `${STORAGE_NAMESPACE}:last-visibility-state`
    };

    const state = {
        identityScheduled: false,
        identityCompleted: false,
        trackingStarted: false,
        trackingInFlight: false,
        heartbeatIntervalId: null,
        visibilityListenerReady: false
    };

    const isTrackingEnabled = () => {
        return window.ADA_RUNTIME_CONFIG?.userSessionTrackingEnabled === true;
    };

    const hasIdentityRegistrationBeenChecked = () => {
        return window.sessionStorage.getItem(STORAGE_KEYS.identityChecked) === 'true';
    };

    const markIdentityRegistrationChecked = () => {
        window.sessionStorage.setItem(STORAGE_KEYS.identityChecked, 'true');
    };

    const hasClientSessionId = () => {
        return Boolean(window.sessionStorage.getItem(STORAGE_KEYS.clientSessionId));
    };

    const hasSessionBeenRegistered = () => {
        return (
            window.sessionStorage.getItem(STORAGE_KEYS.sessionRegistered) === 'true'
            && hasClientSessionId()
        );
    };

    const markSessionRegistered = () => {
        window.sessionStorage.setItem(STORAGE_KEYS.sessionRegistered, 'true');
    };

    const getStoredVisibilityState = () => {
        return window.sessionStorage.getItem(STORAGE_KEYS.lastVisibilityState);
    };

    const setStoredVisibilityState = (visibilityState) => {
        window.sessionStorage.setItem(STORAGE_KEYS.lastVisibilityState, visibilityState);
    };

    const createClientSessionId = () => {
        if (window.crypto && typeof window.crypto.randomUUID === 'function') {
            return window.crypto.randomUUID();
        }

        return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    };

    const getOrCreateClientSessionId = () => {
        const existingClientSessionId = window.sessionStorage.getItem(
            STORAGE_KEYS.clientSessionId
        );

        if (existingClientSessionId) {
            return existingClientSessionId;
        }

        const clientSessionId = createClientSessionId();

        window.sessionStorage.setItem(
            STORAGE_KEYS.clientSessionId,
            clientSessionId
        );

        return clientSessionId;
    };

    const getViewport = () => {
        return {
            width: window.innerWidth,
            height: window.innerHeight
        };
    };

    const buildSessionPayload = (eventType) => {
        return {
            client_session_id: getOrCreateClientSessionId(),
            event_type: eventType,
            pathname: window.location.pathname,
            visibility_state: document.visibilityState,
            viewport: getViewport()
        };
    };

    const postJson = async (url, payload, options = {}) => {
        const response = await fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            keepalive: options.keepalive === true,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        let data = null;

        try {
            data = await response.json();
        } catch {
            data = null;
        }

        return {
            ok: response.ok,
            data
        };
    };

    const sendBeaconJson = (url, payload) => {
        if (!navigator.sendBeacon) {
            return false;
        }

        const blob = new Blob(
            [JSON.stringify(payload)],
            {
                type: 'application/json'
            }
        );

        return navigator.sendBeacon(url, blob);
    };

    const sendSessionEvent = async (eventType, options = {}) => {
        if (!isTrackingEnabled()) {
            return false;
        }

        const payload = buildSessionPayload(eventType);

        if (options.beacon === true && sendBeaconJson(USER_SESSION_TOUCH_URL, payload)) {
            return true;
        }

        try {
            const result = await postJson(
                USER_SESSION_TOUCH_URL,
                payload,
                {
                    keepalive: options.keepalive === true
                }
            );

            return result.ok && result.data?.tracked === true;
        } catch (error) {
            console.warn(`[WARN] User session event failed: ${eventType}`, error);
            return false;
        }
    };

    const registerCurrentUser = async () => {
        if (state.identityCompleted || hasIdentityRegistrationBeenChecked()) {
            state.identityCompleted = true;
            return true;
        }

        const result = await postJson(
            IDENTITY_REGISTER_URL,
            {},
            {
                keepalive: false
            }
        );

        if (!result.ok) {
            return false;
        }

        markIdentityRegistrationChecked();
        state.identityCompleted = true;

        return true;
    };

    const registerSessionIfNeeded = async () => {
        if (!isTrackingEnabled()) {
            return false;
        }

        if (hasSessionBeenRegistered()) {
            return true;
        }

        const ok = await sendSessionEvent('register');

        if (!ok) {
            return false;
        }

        markSessionRegistered();
        setStoredVisibilityState(document.visibilityState);

        return true;
    };

    const stopHeartbeat = () => {
        if (!state.heartbeatIntervalId) {
            return;
        }

        clearInterval(state.heartbeatIntervalId);
        state.heartbeatIntervalId = null;
    };

    const sendHeartbeat = () => {
        if (document.visibilityState !== 'visible') {
            return;
        }

        sendSessionEvent('heartbeat')
            .catch(() => undefined);
    };

    const startHeartbeat = () => {
        if (state.heartbeatIntervalId) {
            return;
        }

        if (document.visibilityState !== 'visible') {
            return;
        }

        state.heartbeatIntervalId = setInterval(() => {
            sendHeartbeat();
        }, HEARTBEAT_MS);
    };

    const handleHidden = () => {
        stopHeartbeat();

        setStoredVisibilityState('hidden');

        sendSessionEvent(
            'hidden',
            {
                beacon: true,
                keepalive: true
            }
        ).catch(() => undefined);
    };

    const handleVisible = () => {
        const previousVisibilityState = getStoredVisibilityState();

        setStoredVisibilityState('visible');

        if (previousVisibilityState === 'hidden') {
            sendSessionEvent('visible')
                .catch(() => undefined);
        } else {
            sendSessionEvent('heartbeat')
                .catch(() => undefined);
        }

        startHeartbeat();
    };

    const handleVisibilityChange = () => {
        if (!state.trackingStarted) {
            if (document.visibilityState === 'visible') {
                startUserSessionTracking()
                    .catch(() => undefined);
            }

            return;
        }

        if (document.visibilityState === 'hidden') {
            handleHidden();
            return;
        }

        if (document.visibilityState === 'visible') {
            handleVisible();
        }
    };

    const ensureVisibilityListener = () => {
        if (state.visibilityListenerReady) {
            return;
        }

        document.addEventListener('visibilitychange', handleVisibilityChange);

        state.visibilityListenerReady = true;
    };

    const startUserSessionTracking = async () => {
        if (!isTrackingEnabled()) {
            return;
        }

        if (state.trackingStarted || state.trackingInFlight) {
            return;
        }

        ensureVisibilityListener();

        if (document.visibilityState !== 'visible') {
            return;
        }

        state.trackingInFlight = true;

        try {
            const registered = await registerSessionIfNeeded();

            if (!registered) {
                return;
            }

            state.trackingStarted = true;

            sendHeartbeat();
            startHeartbeat();
        } finally {
            state.trackingInFlight = false;
        }
    };

    const runIdentityThenTracking = async () => {
        const identityReady = await registerCurrentUser();

        if (!identityReady) {
            return;
        }

        await startUserSessionTracking();
    };

    const scheduleRegistration = () => {
        if (
            state.identityScheduled ||
            (
                state.identityCompleted
                && (
                    state.trackingStarted
                    || !isTrackingEnabled()
                )
            )
        ) {
            return;
        }

        state.identityScheduled = true;

        setTimeout(() => {
            runIdentityThenTracking()
                .catch((error) => {
                    console.warn('[WARN] Identity/session registration failed:', error);
                })
                .finally(() => {
                    state.identityScheduled = false;
                });
        }, IDENTITY_REGISTER_DELAY_MS);
    };

    const boot = () => {
        window.addEventListener(PAGE_LOADER_READY_EVENT, () => {
            scheduleRegistration();
        });

        setTimeout(() => {
            scheduleRegistration();
        }, FALLBACK_DELAY_MS);
    };

    window.ADAIdentityRegistration = {
        retry: () => {
            window.sessionStorage.removeItem(STORAGE_KEYS.identityChecked);

            state.identityCompleted = false;
            state.identityScheduled = false;

            scheduleRegistration();
        },
        clear: () => {
            window.sessionStorage.removeItem(STORAGE_KEYS.identityChecked);

            state.identityCompleted = false;
            state.identityScheduled = false;
        }
    };

    window.ADAUserSessionTracking = {
        retry: () => {
            window.sessionStorage.removeItem(STORAGE_KEYS.sessionRegistered);
            window.sessionStorage.removeItem(STORAGE_KEYS.clientSessionId);
            window.sessionStorage.removeItem(STORAGE_KEYS.lastVisibilityState);

            stopHeartbeat();

            state.trackingStarted = false;
            state.trackingInFlight = false;

            startUserSessionTracking()
                .catch(() => undefined);
        },
        clear: () => {
            window.sessionStorage.removeItem(STORAGE_KEYS.sessionRegistered);
            window.sessionStorage.removeItem(STORAGE_KEYS.clientSessionId);
            window.sessionStorage.removeItem(STORAGE_KEYS.lastVisibilityState);

            stopHeartbeat();

            state.trackingStarted = false;
            state.trackingInFlight = false;
        },
        heartbeat: () => {
            sendHeartbeat();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();