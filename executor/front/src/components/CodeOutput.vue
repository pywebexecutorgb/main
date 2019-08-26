<template>
    <div class="result-block">
        <div class="result form-group">
            <label for="output-result">Result:</label>
            <textarea id="output-result" :class="{'error-message': hasErrors,
                                                  'gray-background': hasNoResult}"
                      readonly v-model="resultView"></textarea>
            <button id="view-button" class="view-button btn btn-secondary" v-show="hasProfile"
                    @click.prevent="changeView">To {{nextViewsValue}}
            </button>
        </div>
    </div>
</template>

<script>
  import methods from '../methods.js';

  export default {
    name: "CodeOutput",

    data() {
      return {
        output: null,
        profile: null,
        hasErrors: false,

        views: ['output', 'profile'],
        indexView: 0,

        // imported methods
        setValues: methods.setValues,
        resetInitData: methods.resetInitData,
      };
    },

    methods: {
      /**
       * Function calculate next possible views Array index
       * @return number, index value
       */
      getNextIndex() {
        return (this.indexView + 1) % this.views.length;
      },

      /**
       * Function get next Index value in views Array
       */
      changeView() {
        this.indexView = this.getNextIndex();
      },
    },

    computed: {
      /**
       * Function check, that output or profile exist,
       *   it's using for gray background output field
       * @return boolean, true - output and profile are empty
       */
      hasNoResult() {
        return !this.output && !this.profile
      },

      /**
       * Function check, that profile result exists
       * @return bool: true if profile not empty and false in other case
       */
      hasProfile() {
        return this.profile && this.profile.length > 0
      },

      /**
       * Return variable content, that name equal views value.
       * If output empty — show cursor only.
       * @return string: output or profile variable content
       */
      resultView() {
        const outputVariableName = this.views[this.indexView];
        return this[outputVariableName];
      },

      /**
       * Function return next value from views array
       * @return string, new view value, like a 'output' or 'profile'
       */
      nextViewsValue() {
        return this.views[this.getNextIndex()];
      }
    },
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        .result-block {
            all: unset !important;
            margin: 0 5px 0 5px;
        }

        .result-block {
            height: 300px !important;
        }

        .btn {
            width: 48% !important;
            margin-right: unset !important;
        }
    }

    .result-block {
        width: 50%;
        height: 600px;
    }

    .result-block {
        margin-left: 5px;
    }

    .result {
        /* profile button use is */
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    #output-result {
        flex-grow: 1;
        font-size: 0.9rem;
        font-family: monospace;
    }

    #output-result {
        border-radius: 3px;
        border: 1px solid lightgray;
        padding: 5px;
        width: 100%;
        display: block;
    }

    .btn {
        width: 130px;
        margin-top: 10px;
        margin-right: 5px;
    }

    .btn:last-child {
        margin-right: 0;
    }

    .view-button {
        position: absolute;
        z-index: 1;
        bottom: 10px;
        right: 10px;

        opacity: 0.95;
    }

    .view-button:hover {
        opacity: 1;
    }

    .gray-background {
        background-color: #f5f5f5;
    }

    .error-message {
        color: darkred;
    }
</style>