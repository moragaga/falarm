(() => {
    const ROOT_PATH = '/';
    const REFRESH_MS = 2 * 60 * 60 * 1000;
    const CHECK_MS = 30 * 1000;

    const state = {
        currentPathname: window.location.pathname,
        rootStartedAt: null,
        pendingRefresh: false,
        intervalId: null
    };

    const isRootPath = () => {
        return window.location.pathname === ROOT_PATH;
    };

    const startRootTimer = () => {
        state.rootStartedAt = Date.now();
        state.pendingRefresh = false;
    };

    const stopRootTimer = () => {
        state.rootStartedAt = null;
        state.pendingRefresh = false;
    };

    const reloadPage = () => {
        window.location.reload();
    };

    const shouldRefresh = () => {
        if (!isRootPath()) {
            return false;
        }

        if (state.rootStartedAt === null) {
            return false;
        }

        return Date.now() - state.rootStartedAt >= REFRESH_MS;
    };

    const syncRouteState = () => {
        const pathname = window.location.pathname;

        if (pathname === state.currentPathname) {
            return;
        }

        state.currentPathname = pathname;

        if (isRootPath()) {
            startRootTimer();
            return;
        }

        stopRootTimer();
    };

    const checkRefresh = () => {
        try {
            syncRouteState();

            if (!isRootPath()) {
                return;
            }

            if (state.rootStartedAt === null) {
                startRootTimer();
                return;
            }

            if (!shouldRefresh()) {
                return;
            }

            if (document.visibilityState !== 'visible') {
                state.pendingRefresh = true;
                return;
            }

            reloadPage();
        } catch (error) {
            console.error('[ERROR] Root auto refresh failed:', error);
        }
    };

    const handleVisibilityChange = () => {
        if (!state.pendingRefresh) {
            return;
        }

        if (!isRootPath()) {
            state.pendingRefresh = false;
            return;
        }

        if (document.visibilityState === 'visible') {
            reloadPage();
        }
    };

    const boot = () => {
        if (isRootPath()) {
            startRootTimer();
        }

        state.intervalId = setInterval(checkRefresh, CHECK_MS);

        document.addEventListener('visibilitychange', handleVisibilityChange);

        checkRefresh();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();