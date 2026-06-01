let wakeLock = null;

const requestWakeLock = async () => {
    if ('wakeLock' in navigator) {
        try {
            wakeLock = await navigator.wakeLock.request('screen');

            wakeLock.addEventListener('release', () => {
                console.log('[INFO] Wake Lock released');
            });
            console.log('[INFO] Wake Lock acquired');
        } catch (err) {
            console.error('[ERROR] not acquiring wake lock:', err);
        }
    } else {
        console.error('[ERROR] Wake Lock API is not supported in this browser');
    }
}

requestWakeLock();

document.addEventListener('visibilitychange', async () => {
    if (wakeLock !== null && document.visibilityState === 'visible') {
        await requestWakeLock();
    }
})