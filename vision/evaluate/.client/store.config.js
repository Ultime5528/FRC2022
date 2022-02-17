const CONFIG_ACTIONS = Object.freeze({
    SET_HEIGHT: "SET_HEIGHT",
})

const configStoreModule = {
    state: {
        height: 250,
    },
    mutations: {
        [CONFIG_ACTIONS.SET_HEIGHT] (state, height) {
            state.height = parseInt(height);
        }
    },
    getters: {
        height: (state) => state.height
    }
}
