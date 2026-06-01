(() => {
    const FADE_OUT_MS = 2000;
    const SYNC_DELAY_MS = 0;
    const MAX_LOADING_MS = 30000;
    const PAGE_LOADER_READY_EVENT = 'ada:page-loader-ready';

    const state = {
        syncTimeout: null,
        observer: null,
        intervalId: null
    };

    const getLoaderScopes = () => {
        return Array.from(document.querySelectorAll('[data-page-loader="true"]'));
    };

    const getReadyElements = (scope) => {
        if (!scope) {
            return [];
        }

        return Array.from(scope.querySelectorAll('[data-ready]'));
    };

    const getPendingReadyElements = (scope) => {
        return getReadyElements(scope).filter((element) => {
            return element.getAttribute('data-ready') !== 'true';
        });
    };

    const getLoaderState = (scope) => {
        return scope.getAttribute('data-loader-state');
    };

    const setLoaderState = (scope, value) => {
        scope.setAttribute('data-loader-state', value);
    };

    const createRunId = () => {
        return String(Date.now()) + '-' + String(Math.random()).slice(2);
    };

    const setRunId = (scope, runId) => {
        scope.setAttribute('data-loader-run-id', runId);
    };

    const getRunId = (scope) => {
        return scope.getAttribute('data-loader-run-id');
    };

    const isStaleLoadedScope = (scope) => {
        const currentState = getLoaderState(scope);

        /*
         * Caso típico al volver desde otra página:
         * Dash reinyecta className="page-loader-scope is-loading",
         * pero el atributo JS data-loader-state quedó como "loaded".
         *
         * Eso deja la página atrapada porque CSS oculta el contenido
         * y el JS cree que ya terminó.
         */
        return currentState === 'loaded' && scope.classList.contains('is-loading');
    };

    const resetScopeToLoading = (scope) => {
        const runId = createRunId();

        setRunId(scope, runId);
        setLoaderState(scope, 'loading');

        scope.setAttribute('data-loader-started-at', String(performance.now()));
        scope.setAttribute('data-loader-log-printed', 'false');
        scope.setAttribute('data-loader-ready-notified', 'false');

        scope.classList.add('is-loading');
        scope.classList.remove('is-fading');
        scope.classList.remove('is-loaded');

        return runId;
    };

    const startLoader = (scope) => {
        const currentState = getLoaderState(scope);

        if (currentState && !isStaleLoadedScope(scope)) {
            return;
        }

        resetScopeToLoading(scope);
    };

    const areReadyElementsLoaded = (scope) => {
        const elements = getReadyElements(scope);

        /*
         * Array.every([]) devuelve true.
         * Por eso exigimos al menos un data-ready.
         */
        if (elements.length === 0) {
            return false;
        }

        return elements.every((element) => {
            return element.getAttribute('data-ready') === 'true';
        });
    };

    const printLoadTimeOnce = (scope) => {
        const alreadyPrinted = scope.getAttribute('data-loader-log-printed') === 'true';

        if (alreadyPrinted) {
            return;
        }

        const startedAt = Number(scope.getAttribute('data-loader-started-at'));

        if (Number.isNaN(startedAt)) {
            return;
        }

        const durationSeconds = (performance.now() - startedAt) / 1000;

        console.log('[INFO] Total time to load: ' + durationSeconds.toFixed(0) + 's');

        scope.setAttribute('data-loader-log-printed', 'true');
    };

    const notifyPageLoaderReadyOnce = (scope) => {
        const alreadyNotified = scope.getAttribute('data-loader-ready-notified') === 'true';

        if (alreadyNotified) {
            return;
        }

        scope.setAttribute('data-loader-ready-notified', 'true');

        window.dispatchEvent(
            new CustomEvent(PAGE_LOADER_READY_EVENT, {
                detail: {
                    loaderKey: scope.getAttribute('data-loader-key'),
                    runId: getRunId(scope)
                }
            })
        );
    };

    const finishLoader = (scope) => {
        const currentState = getLoaderState(scope);

        if (currentState === 'fading' || currentState === 'loaded') {
            return;
        }

        const runId = getRunId(scope);

        setLoaderState(scope, 'fading');

        /*
         * Primero mostramos el contenido.
         * El overlay sigue encima, por eso no hay salto visual.
         */
        scope.classList.remove('is-loading');
        scope.classList.add('is-fading');
        scope.classList.remove('is-loaded');

        window.requestAnimationFrame(() => {
            window.setTimeout(() => {
                if (!document.body.contains(scope)) {
                    return;
                }

                /*
                 * Evita que un timeout viejo modifique un loader nuevo.
                 */
                if (getRunId(scope) !== runId) {
                    return;
                }

                printLoadTimeOnce(scope);

                scope.classList.remove('is-fading');
                scope.classList.remove('is-loading');
                scope.classList.add('is-loaded');

                setLoaderState(scope, 'loaded');
                notifyPageLoaderReadyOnce(scope);
            }, FADE_OUT_MS);
        });
    };

    const hasLoadingTimedOut = (scope) => {
        const currentState = getLoaderState(scope);

        if (currentState !== 'loading') {
            return false;
        }

        const startedAt = Number(scope.getAttribute('data-loader-started-at'));

        if (Number.isNaN(startedAt)) {
            return false;
        }

        return performance.now() - startedAt > MAX_LOADING_MS;
    };

    const forceFinishExpiredLoader = (scope) => {
        const pendingElements = getPendingReadyElements(scope);

        const pendingIds = pendingElements.map((element) => {
            return element.id || element.getAttribute('data-ready-name') || element.tagName;
        });

        console.warn(
            '[WARN] Page loader timeout. Pending data-ready elements:',
            pendingIds
        );

        finishLoader(scope);
    };

    const syncPageLoaders = () => {
        const scopes = getLoaderScopes();

        scopes.forEach((scope) => {
            startLoader(scope);

            if (areReadyElementsLoaded(scope)) {
                finishLoader(scope);
                return;
            }

            /*
             * Fallback defensivo:
             * evita que la app quede atrapada para siempre si algún callback
             * no vuelve a marcar data-ready="true".
             */
            if (hasLoadingTimedOut(scope)) {
                forceFinishExpiredLoader(scope);
            }
        });
    };

    const requestSync = () => {
        if (state.syncTimeout) {
            return;
        }

        state.syncTimeout = window.setTimeout(() => {
            state.syncTimeout = null;

            try {
                syncPageLoaders();
            } catch (error) {
                console.error('[ERROR] Page loader failed:', error);
            }
        }, SYNC_DELAY_MS);
    };

    const startObserver = () => {
        if (state.observer) {
            return;
        }

        state.observer = new MutationObserver(() => {
            requestSync();
        });

        state.observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: [
                'data-ready',
                'class',
                'data-page-loader'
            ]
        });
    };

    const startInterval = () => {
        if (state.intervalId) {
            return;
        }

        /*
         * Revisión periódica liviana.
         * Esto cubre casos donde Dash cambia cosas sin disparar
         * una mutación útil para el loader, o donde un data-ready
         * queda pendiente para siempre.
         */
        state.intervalId = window.setInterval(() => {
            requestSync();
        }, 1000);
    };

    const boot = () => {
        startObserver();
        requestSync();
        startInterval();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();