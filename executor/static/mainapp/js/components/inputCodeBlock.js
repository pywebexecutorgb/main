"use strict";

const inputCodeBlock = {
  data() {
    return {
      code: '',
      requirements: '',
      url: null,
    };
  },

  template: `
        <div class="input-block">
            <div id="loader" hidden="hidden"></div>
            <input id="url-result" type="text" hidden>

            <div id="code_create_form" class="input-form" >
                <label for="id_code_text">Code text:</label>
                <textarea id="id_code_text" name="code_text" class="form-control"
                           v-model="code" cols="40" rows="10"  maxlength="2048" required=""></textarea>
                <label for="id_dependencies">Requirements.txt:</label>
                <textarea id="id_dependencies" name="dependencies" class="form-control"
                          v-model="requirements" cols="40" rows="3" maxlength="256"></textarea>

                <div class="buttons">
                    <button id="execute_button" class="run-button btn btn-outline-success" type="submit"
                            @click.prevent="executeCode($event)">
                        Execute code
                    </button>
                    <button id="save-button" class="save-button btn btn-outline-secondary"
                            @click.prevent="executeCode($event, true)">
                        Save
                    </button>
                    <button id="copy-button" class="copy-button btn btn-outline-secondary"
                        @click.prevent="copyURL($event)">
                        Copy URL
                    </button>
                    <button type="reset" value="Reset" class="clear-button btn btn-outline-secondary"
                        @click.prevent="resetInitData">
                        Clear form
                    </button>
                </div>
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
     * Show spinner and make button inactive again.
     * @param event
     */
    enableProcessing(event) {
      document.getElementById('loader').hidden = false;

      event.target.dataset.defaultValue = event.target.textContent;
      event.target.textContent = 'Processing...';
      event.target.disabled = true;
    },

    /**
     * Hide spinner and make button active again.
     * @param event
     */
    disableProcessing(event) {
      event.target.textContent = event.target.dataset.defaultValue;
      event.target.disabled = false;

      document.getElementById('loader').hidden = true;
    },

    /**
     * Execute code logic:
     * if containderID is defined and action = execute, execute command in containerID
     * else call save API location.
     * @param event
     * @param isSave {boolean} - operation flag
     * @return {Promise}, don't wait answer, v-model make magic with variables
     */
    async executeCode(event, isSave = false) {
      this.enableProcessing(event);

      const body = JSON.stringify({
        code_text: this.code,
        dependencies: this.requirements,
      });

      const containerID = sessionStorage.getItem('containerID');
      let url = this.$parent.getURL('saveCode');
      if (!isSave && containerID) {
        url = this.$parent.getURL('execCode', containerID);
      }

      try {
        await this.$parent.getJSON(url, {
          body,
          method: 'POST',
          headers: {'Content-Type': 'application/json'}
        })
          .then(data => {
            this.$parent.$refs.output.resetInitData();

            // update URL if we've received url value (only when save)
            if (isSave && data.hasOwnProperty('code')) {
              this.url = data['code']['url'];
              history.pushState('update URL', '', window.location.origin + this.url);
            }

            this.$parent.$refs.output.setValues({
              output: data['output'],
              profile: data['profile'],
              hasErrors: data['has_errors'],
            });
          });
      } catch (error) {
        this.$parent.$refs.error.setMessage(`Cannot execute command: ${error.message}`);
      }

      this.disableProcessing(event);
    },

    /**
     * Copy URL logic:
     * - get URL from data domain and location in #url-result (return from backend)
     * - set input unhidden
     * - select all text in input
     * - copy string into clipboard
     * - make input hidden again
     * Also added logic: make copy button inactive for 2 sec.
     * @param event
     */
    copyURL(event) {
      let urlInput = document.getElementById('url-result');
      urlInput.value = window.location.origin + this.url;
      urlInput.hidden = false;
      urlInput.select();
      document.execCommand('copy');
      urlInput.blur();
      urlInput.hidden = true;

      event.target.dataset.defaultValue = event.target.textContent;
      event.target.textContent = 'URL copied';
      event.target.disabled = true;

      setTimeout(() => {
        event.target.textContent = event.target.dataset.defaultValue;
        event.target.disabled = false;
      }, 2000);
    },
  },
};
