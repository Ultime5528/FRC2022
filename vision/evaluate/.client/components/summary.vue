<template>
  <v-container fluid class="gallery" :style="galleryStyle">
    <v-card
      v-for="(photo, index) in photos"
      :key="photo.name"
      :loading="photo.loading"
      rounded="lg"
      class="gallery-item">
      <template slot="progress">
        <v-progress-linear
          color="primary"
          height="10"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-card-title>{{ photo.name }}</v-card-title>

      <lightbox-img
        :src="photo.data"
        :max-height="height"
        contain
      ></lightbox-img>
    </v-card>
  </v-container>
</template>


<style>

</style>


<script>
module.exports = {
  components: {
    "lightbox-img": httpVueLoader("./lightbox-img.vue"),
  },
  computed: {
    galleryStyle: function() {
      return {
        "display": "grid",
        "grid-gap": "10px",
        "grid-template-columns": "repeat(auto-fill, minmax(" + this.height + "px, 1fr))"
      }
    },
    height () {
      return this.$store.getters.height;
    },
    photos() {
      return this.$store.getters.photos;
    }
  },
};
</script>
