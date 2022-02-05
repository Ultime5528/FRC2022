<template>
    <div>
        <v-img :src="src" v-bind="$attrs" class="lightbox-img" @click="overlay = true"></v-img>
        <v-overlay :value="overlay">
            <div class="lightbox-container">
                <v-btn
                    plain
                    elevation="0"
                    class="lightbox-close-btn"
                    @click="overlay = false">ESC <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-img
                    v-hotkey="keymap"
                    v-click-outside="hideOverlay"
                    :src="src"
                    contain
                    width="100%"
                    height="100%"
                />
            </div>
        </v-overlay>
    </div>
</template>

<style>
.lightbox-img {
    cursor: pointer;
}

.overlay-lightbox-img {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    max-width: 100%;
    max-height: 100%;
    margin: auto;
}

.lightbox-container {
    width: 100vw;
    height: 100vh;
    padding: 100px;
}

.lightbox-close-btn {
    position: absolute;
    top: 30px;
    right: 30px;
}
</style>

<script>
module.exports = {
    props: ["src"],
    data: function () {
        return {
            overlay: false,
        };
    },
    methods: {
        hideOverlay() {
            this.overlay = false;
        }
    },
    computed: {
        keymap() {
            return {
                "esc": this.hideOverlay
            }
        }
    },
}
</script>
