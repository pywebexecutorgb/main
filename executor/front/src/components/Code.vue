<template>
    <div class="content">
        <CodeError ref="error"></CodeError>
        <code-input ref="input"></code-input>
        <code-output ref="output"></code-output>
    </div>
</template>

<script>
  import methods from '../methods.js';

  import CodeInput from './CodeInput.vue';
  import CodeOutput from './CodeOutput.vue';
  import CodeError from './CodeError.vue';

  export default {
    name: "Code",
    props: ['pk'],

    data() {
      return {
        // imported methods
        getURL: methods.getURL,
        getJSON: methods.getJSON,
      }
    },

    components: {
      CodeInput,
      CodeOutput,
      CodeError
    },

    mounted() {
      this.defineCodeByID();
    },

    methods: {
      /**
       * Function read router param = pk
       * and try to get exist values for executed code throw API.
       */
      defineCodeByID() {
        if (!this.pk) {
          return null;
        }

        const url = this.getURL('readCode', this.pk);
        this.getJSON(url)
          .then(data => {
            this.$refs.input.setValues({
              code: data['code']['code_text'],
              requirements: data['code']['dependencies'],
              url: data['code']['url'],
            });

            this.$refs.output.resetInitData();
            this.$refs.output.setValues({
              output: data['output'],
              profile: data['profile'],
              hasErrors: data['has_errors'],
            });
          })
          .catch(error => this.$store.commit('setError',
            `Cannot fetch executed code ID ${this['pk']}: ${error.message}`));
      },
    },
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        .content {
            display: flex;
            flex-direction: column;
            height: unset !important;
            min-height: 800px;
        }
    }

    .content {
        display: flex;
        height: 100%;
    }
</style>