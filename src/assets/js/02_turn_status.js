(() => {
    const getNext19 = (now = new Date()) => {
        const next = new Date(now);

        next.setHours(19, 0, 0, 0);

        if (now >= next) {
            next.setDate(next.getDate() + 1);
        }

        return next;
    };

    const formatTime = (ms) => {
        const totalSeconds = Math.max(0, Math.floor(ms / 1000));

        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return {
            hours: String(hours).padStart(2, '0'),
            minutes: String(minutes).padStart(2, '0'),
            seconds: String(seconds).padStart(2, '0')
        };
    };

    const startCountdown = (elementSelector) => {
        const el = document.querySelector(elementSelector);

        if (!el) {
            return null;
        }

        if (!window.AppSecondTicker) {
            console.error('[ERROR] AppSecondTicker is not available for countdown');
            return null;
        }

        const update = (now) => {
            const next19 = getNext19(now);
            const diff = next19 - now;
            const { hours, minutes, seconds } = formatTime(diff);

            el.textContent = `${hours}:${minutes}:${seconds}`;
        };

        return window.AppSecondTicker.subscribe(update);
    };

    loadedComponent(
        '#header-ready-flag-status',
        () => {
            return startCountdown('#header-status-remaining-hours');
        },
        {
            label: 'header countdown'
        }
    );
})();