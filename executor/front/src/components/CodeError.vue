<template>
    <div class="error bg-danger" v-show="error">
        {{error}}
    </div>
</template>

<script>
  export default {
    name: "CodeError",

    computed: {
      error() {
        return this.$store.getters.getError;
      },
    },
  }
</script>

<style scoped>
    .error {
        position: fixed;
        z-index: 1;
        top: 7%;

        color: whitesmoke;
        text-align: center;
        min-width: 250px;
        max-width: 400px;

        border-radius: 3px;
        padding: 0 5px;
        /* using 15px padding upstairs */
        margin: 0 25px 0 10px;
    }
</style>