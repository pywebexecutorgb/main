<template>
    <div class="input-block">
        <div id="loader" hidden="hidden"></div>
        <input id="url-result" type="text" hidden>

        <div id="code_create_form" class="input-form">
            <label for="id_code_text">Code text:</label>
            <codemirror id="id_code_text" name="code_text" maxlength="2048" required=""
                        v-model="code" :options="cmOption" ref="codeText"></codemirror>

            <label for="id_dependencies">Requirements.txt:</label>
            <textarea id="id_dependencies" name="dependencies" class="form-control"
                      v-model="requirements" cols="40" rows="3" maxlength="256"></textarea>

            <div class="buttons">
                <button id="execute_button" class="run-button btn btn-outline-success" type="submit"
                        @click.prevent="executeCode($event)">
                    Execute
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
    </div>
</template>

<script>
  import methods from '../methods.js';

  import 'codemirror/lib/codemirror.css';
  import 'codemirror/mode/python/python.js';
  import {codemirror} from 'vue-codemirror';

  export default {
    name: "CodeInput",
    components: {
      codemirror
    },

    data() {
      return {
        code: '',
        requirements: '',
        url: null,

        cmOption: {
          mode: {
            name: "python",
            version: 3,
            singleLineStringErrors: false
          },
          indentUnit: 4,
        },

        // imported methods
        getCookie: methods.getCookie,
        setValues: methods.setValues,
        resetInitData: methods.resetInitData,
      };
    },

    mounted() {
      this.$refs.codeText.codemirror.setSize("100%", "100%");
    },

    methods: {
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

        const csrfToken = this.getCookie('csrftoken');
        try {
          await this.$parent.getJSON(url, {
            credentials: 'include',
            body,
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            }
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
          this.$store.commit('setError', `Cannot execute command: ${error.message}`);
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
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        .input-block {
            all: unset !important;
            margin: 0 5px 0 5px;
        }

        .buttons {
            display: flex;
            flex-wrap: wrap;
        }

        .btn {
            width: 48% !important;
            margin-right: unset !important;
        }

        #id_code_text {
            height: 250px !important;
            padding: 3px !important;
        }
    }

    .vue-codemirror {
        border-radius: 3px;
        border: 1px solid lightgray;
    }

    .input-block {
        width: 50%;
        height: 600px;
    }

    .input-block {
        /* spinner use it */
        position: relative;
        margin-right: 5px;
    }

    .input-form {
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    #id_code_text {
        flex-grow: 1;
        font-size: 0.9rem;
        font-family: monospace;
        padding: 3px !important;

        height: 400px;
    }

    #id_dependencies {
        font-size: 0.9rem;
        font-family: monospace;
    }

    .buttons {
        display: flex;
        justify-content: space-between;
    }

    .btn {
        width: 130px;
        margin-top: 10px;
        margin-right: 5px;
    }

    .btn:last-child {
        margin-right: 0;
    }

    #loader {
        position: absolute;
        top: 25%;
        left: 40%;
        width: 100px;
        height: 100px;

        border: 10px solid lightgray;
        border-top-color: darkgrey;
        border-radius: 50%;

        animation: 2s infinite linear spin;
        z-index: 1;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>