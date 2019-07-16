"use strict";

const codeBlock = {
    props: ['pk'],

    components: {
      errorCodeBlock,
      inputCodeBlock,
      outputCodeBlock,
    },

    template: `
        <div class="content">
            <error-code-block ref="error"></error-code-block>
            <input-code-block ref="input"></input-code-block>
            <output-code-block ref="output"></output-code-block>
        </div>`,

    methods: {
      /**
       * Function read router param = pk
       * and try to get exist values for executed code throw API.
       */
      defineCodeByID() {
        if (!this['pk']) {
          return null;
        }

        const url = this.getURL('readCode', this['pk']);
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
          });
      },

      /**
       * Main URL API logic: return URL string by input params.
       * @param name, {string} - action name
       * @param param, {string} - param is container ID
       * @return url, {string}
       */
      getURL(name, param = null) {
        switch (name) {
          case 'createContainer':
            return '/api/containers/';
          case 'saveCode':
            return '/api/code-bases/';
          case 'execCode':
            return `/api/containers/${param}/codes/`;
          case 'readCode':
            return `/api/code-executions/${param}/`;
          case 'changeContainer':
            return `/api/containers/${param}/`;
        }
      },

      /**
       * Function make URL request and parse JSON answer
       * @param url, string
       * @param params, fetch {Object}
       * @return {Promise}, fetch promise
       */
      getJSON(url, params = {}) {
        return fetch(url, params)
          .then(response => response.json())
          .catch(error => console.log(error))
      },

      /**
       * Function create container on created Vue add:
       * make POST request to REST API
       */
      createContainer() {
        this.getJSON(this.getURL('createContainer'), {
          method: 'POST',
          headers: {'Content-Type': 'application/json'}
        })
          .then(data => sessionStorage.setItem('containerID', data['container_id']));
      },
      /**
       * Remove container on beforeunload action.
       */
      deleteContainer() {
        const containerID = sessionStorage.getItem('containerID');
        if (!containerID) {
          return null;
        }
        fetch(this.getURL('changeContainer', containerID), {method: 'DELETE'});
      },

      /**
       * Function send PUT request in timeout interval,
       * by timestamp value we removed unused containers on backend side.
       */
      sendHealthCheck() {
        const containerID = sessionStorage.getItem('containerID');
        if (!containerID) {
          return null;
        }

        fetch(this.getURL('changeContainer', containerID), {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'date': Date.now()}),
        })
          .then((response) => {
            if (response.status !== 204) {
              throw new Error('received wrong status code');
            }
            this.$refs.error.resetInitData();
          })
          .catch((error) => this.$refs.error.setMessage(
            `Error while send container healthcheck, please refresh page. Detail: "${error.message}"`));
      },
    },

    created() {
      this.createContainer();
      setInterval(this.sendHealthCheck, 10000);

      window.addEventListener('unload', this.deleteContainer());
    },

    mounted() {
      this.defineCodeByID();
    }
  }
;