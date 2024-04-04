

export function onDomLoaded(callback) {
    if (document.readyState !== 'loading') {
        try {
            callback();
        } catch (error) {
            console.error(error);
        }
        return;
    }
    let _complete = false;
    document.addEventListener('DOMContentLoaded', () => {
        if (_complete) {
            return;
        }
        _complete = true;
        callback();
    });
}
