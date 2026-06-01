(() => {
    const getCurrentDateTime = (now = new Date()) => {
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    };

    const startCurrentDateTime = (elementSelector) => {
        const el = document.querySelector(elementSelector);

        if (!el) {
            return null;
        }

        if (!window.AppSecondTicker) {
            console.error('[ERROR] AppSecondTicker is not available for current datetime');
            return null;
        }

        const update = (now) => {
            el.textContent = getCurrentDateTime(now);
        };

        return window.AppSecondTicker.subscribe(update);
    };

    loadedComponent(
        '#information-ready-flag',
        () => {
            return startCurrentDateTime('#information-time-now');
        },
        {
            label: 'information current datetime'
        }
    );
})();