const PHOTOS_ACTIONS = Object.freeze({
    SET_PHOTO_NAMES: "SET_PHOTO_NAMES",
    SET_PHOTO_DATA: "SET_PHOTO_DATA",
})

createLoadingPhotoFromName = (name) => ({
    name: name,
    loading: true,
    data: null,
})

const visionStoreModule = {
    state: {
        photos: []
    },
    mutations: {
        [PHOTOS_ACTIONS.SET_PHOTO_NAMES] (state, filenames) {
            state.photos = filenames.map(createLoadingPhotoFromName);
        },

        [PHOTOS_ACTIONS.SET_PHOTO_DATA] (state, payload) {
            let photos = state.photos.filter(p => p.name === payload.name);

            if (photos.length === 1) {
                photos[0].data = payload.data;
                photos[0].loading = false;
            } else {
                console.error("There should be only one photo with name", payload.name);
            }
        }
    },
    getters: {
        photos: (state) => state.photos,
    }
}
