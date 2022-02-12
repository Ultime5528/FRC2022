<template>
  <h3>{{ title }}</h3>
</template>

<style>
h3 {
  background-color: green;
}
</style>

<script>
module.exports = {
  props: ["title"],
};
</script>
