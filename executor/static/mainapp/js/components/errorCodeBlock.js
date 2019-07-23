"use strict";

const errorCodeBlock = {
  data() {
    return {
      message: null,
    }
  },

  template: `
    <div class="error bg-danger" v-show="message">
        {{message}}
    </div>`,

  methods: {
    /**
     * Function reset data values
     */
    resetInitData() {
      Object.assign(this.$data, this.$options.data.apply(this));
    },

    /**
     * Define error message
     * @param value, {string} - message value
     */
    setMessage(value) {
      this.message = value;
    }
  },
};
