if (window.eel === undefined) {
    window.eel = {
        expose (...args) {
            console.warn("eel.expose", args);
        },
        eval(...args) {
            console.warn("eel.eval", args);
        }
    }
}
