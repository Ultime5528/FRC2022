Vue.use(httpVueLoader);
Vue.use(window["v-hotkey"]["default"]);


let store = new Vuex.Store({
  modules: {
    config: configStoreModule,
    photos: visionStoreModule,
  }
})


eel.expose(setPhotoNames)
function setPhotoNames(fileNames) {
  store.commit(PHOTOS_ACTIONS.SET_PHOTO_NAMES, fileNames);
}

eel.expose(setPhotoData)
function setPhotoData(payload) {
  store.commit(PHOTOS_ACTIONS.SET_PHOTO_DATA, payload);
}


window.vue = new Vue({
  el: "#app",
  components: {
    "demo-component": "url:components/demo.vue",
    "lightbox-img": "url:components/lightbox-img.vue",
    "summary-component": "url:components/summary.vue",
  },
  data: {
    tab: null,
    tabs: ["Résumé", "Détails", "Métriques"],
    showOptions: false,
  },
  store: store,
  computed: {
    height: {
      get() {
        return this.$store.getters.height;
      },
      set (newValue) {
        this.$store.commit(CONFIG_ACTIONS.SET_HEIGHT, parseInt(newValue));
      }
    },
  },
  vuetify: new Vuetify({
    theme: {
      dark: false,
      themes: {
        light: {
          primary: "#3f51b5",
          secondary: "#2196f3",
          accent: "#ff9800",
          error: "#f44336",
          warning: "#ffc107",
          info: "#03a9f4",
          success: "#4caf50",
        },
      },
    },
  })
});

eel.eval()
