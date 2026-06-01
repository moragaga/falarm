(() => {
    const registry = [];

    const supportState = {
        observer: null,
        syncTimeout: null
    };

    const requestSync = () => {
        if (supportState.syncTimeout) {
            return;
        }

        supportState.syncTimeout = setTimeout(() => {
            supportState.syncTimeout = null;
            syncLoadedComponents();
        }, 0);
    };

    const cleanupRemovedElements = (entry) => {
        entry.activeElements.forEach((element) => {
            if (document.body.contains(element)) {
                return;
            }

            const cleanup = entry.cleanupByElement.get(element);

            if (typeof cleanup === 'function') {
                try {
                    cleanup();
                } catch (error) {
                    console.error('[ERROR] loadedComponent cleanup failed:', entry.label, error);
                }
            }

            entry.activeElements.delete(element);
            entry.cleanupByElement.delete(element);
        });
    };

    const executeEntry = (entry, element) => {
        if (entry.executedElements.has(element)) {
            return;
        }

        if (element.getAttribute(entry.readyAttribute) !== entry.readyValue) {
            return;
        }

        entry.executedElements.add(element);
        entry.activeElements.add(element);

        try {
            const cleanup = entry.callback(element);

            if (typeof cleanup === 'function') {
                entry.cleanupByElement.set(element, cleanup);
            }
        } catch (error) {
            console.error('[ERROR] loadedComponent callback failed:', entry.label, error);
        }
    };

    const syncLoadedComponents = () => {
        registry.forEach((entry) => {
            cleanupRemovedElements(entry);

            const elements = Array.from(document.querySelectorAll(entry.selector));

            elements.forEach((element) => {
                executeEntry(entry, element);
            });
        });
    };

    const startObserver = () => {
        if (supportState.observer) {
            return;
        }

        supportState.observer = new MutationObserver(() => {
            requestSync();
        });

        supportState.observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: [
                'data-ready',
                'class'
            ]
        });
    };

    window.loadedComponent = (selector, callback, options = {}) => {
        const entry = {
            selector: selector,
            callback: callback,
            label: options.label || selector,
            readyAttribute: options.readyAttribute || 'data-ready',
            readyValue: options.readyValue || 'true',
            executedElements: new WeakSet(),
            activeElements: new Set(),
            cleanupByElement: new Map()
        };

        registry.push(entry);

        startObserver();
        requestSync();

        return {
            stop: () => {
                const index = registry.indexOf(entry);

                if (index >= 0) {
                    registry.splice(index, 1);
                }

                entry.activeElements.forEach((element) => {
                    const cleanup = entry.cleanupByElement.get(element);

                    if (typeof cleanup === 'function') {
                        try {
                            cleanup();
                        } catch (error) {
                            console.error('[ERROR] loadedComponent cleanup failed:', entry.label, error);
                        }
                    }
                });

                entry.activeElements.clear();
                entry.cleanupByElement.clear();
            }
        };
    };

    const tickerState = {
        subscribers: new Set(),
        timeoutId: null,
        started: false
    };

    const getCurrentSecondDate = () => {
        const timestamp = Date.now();
        const roundedTimestamp = timestamp - (timestamp % 1000);

        return new Date(roundedTimestamp);
    };

    const emitClockTick = () => {
        const now = getCurrentSecondDate();

        tickerState.subscribers.forEach((callback) => {
            try {
                callback(now);
            } catch (error) {
                console.error('[ERROR] AppSecondTicker callback failed:', error);
            }
        });
    };

    const scheduleNextTick = () => {
        if (!tickerState.started) {
            return;
        }

        const delayToNextSecond = 1000 - (Date.now() % 1000);

        tickerState.timeoutId = setTimeout(() => {
            tickerState.timeoutId = null;

            emitClockTick();
            scheduleNextTick();
        }, delayToNextSecond);
    };

    const startTicker = () => {
        if (tickerState.started) {
            return;
        }

        tickerState.started = true;
        scheduleNextTick();
    };

    const stopTickerIfUnused = () => {
        if (tickerState.subscribers.size > 0) {
            return;
        }

        if (tickerState.timeoutId) {
            clearTimeout(tickerState.timeoutId);
            tickerState.timeoutId = null;
        }

        tickerState.started = false;
    };

    window.AppSecondTicker = {
        subscribe: (callback) => {
            tickerState.subscribers.add(callback);
            startTicker();

            try {
                callback(getCurrentSecondDate());
            } catch (error) {
                console.error('[ERROR] AppSecondTicker initial callback failed:', error);
            }

            return () => {
                tickerState.subscribers.delete(callback);
                stopTickerIfUnused();
            };
        }
    };

    const boot = () => {
        startObserver();
        requestSync();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();