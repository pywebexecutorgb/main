"use strict";

const outputCodeBlock = {
  data() {
    return {
      output: null,
      profile: null,
      hasErrors: false,

      views: ['output', 'profile'],
      indexView: 0,
    };
  },

  template: `
          <div class="result-block">
            <div class="result form-group">
                <label for="output-result">Result:</label>
                <textarea id="output-result" :class="{'error-message': hasErrors,
                                                      'blinking': hasNoResult}" readonly>&#9646; {{resultView}}</textarea>
                <button id="view-button" class="view-button btn btn-secondary" v-show="hasProfile"
                    @click.prevent="changeView">To {{nextViewsValue}}</button>
            </div>
        </div>`,

  methods: {
    /**
     * Update data values with input object — assign
     * @param {Object}, valuesObject
     */
    setValues(valuesObject) {
      Object.assign(this, valuesObject);
    },

    /**
     * Function reset data values
     */
    resetInitData() {
      Object.assign(this.$data, this.$options.data.apply(this));
    },

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
     *   it's using in blinking text
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
     * Return variable content, that name equal views value
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
};
