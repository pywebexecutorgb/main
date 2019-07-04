"use strict";

window.addEventListener('load', () => {
    clearButtonListener();
    saveButtonListener();
    copyButtonListener();

    /**
     * Function setup empty values for text in forms by click "clear button"
     */
    function clearButtonListener() {
      let btn = document.querySelector('.clear-button');
      btn.addEventListener('click', () => {
        resetInputForm();
      });

      /**
       * Change form fields text to empty
       */
      function resetInputForm() {
        document.getElementById('id_code_text').textContent = '';
        document.getElementById('id_dependencies').textContent = '';
      }
    }

    function saveButtonListener() {
      let saveBtn = document.getElementById('save-button');
      saveBtn.addEventListener('click', (event) => {
        event.preventDefault();
        saveCode(event);
      });

      async function saveCode(event) {
        enableProcessingSaving();

        const postForm = document.getElementById('code_create_form');
        await fetch('/api/code-bases/', {
          method: 'POST',
          body: new FormData(postForm),
        })
          .then(result => result.json())
          .then((result) => {
            successSaveCallback(result);
          })
          .catch((result) => {
            errorSaveCallback(result);
          });

        disableProcessingSaving();
      }
    }

    function enableProcessingSaving() {
      document.getElementById('loader').hidden = false;

      const saveButton = document.getElementById('save-button');
      saveButton.dataset.defaultValue = saveButton.textContent;
      saveButton.textContent = 'Saving...';
      saveButton.disabled = true;
    }

    function successSaveCallback(data) {
      const outputResult = document.getElementById('output-result');
      outputResult.value = data['output'];
      if (!data['has_errors']) {
        outputResult.classList.remove('error-message');
      } else {
        outputResult.classList.add('error-message');
      }
      outputResult.classList.remove('blinking');

      // update location result and address bar
      let url = document.getElementById('url-result');
      url.dataset.location = data['code']['url'];

      history.pushState('update URL', '', window.location.origin + url.dataset.location);
    }

    function errorSaveCallback(data) {
      const outputResult = document.getElementById('output-result');
      outputResult.value = data.responseText;
      outputResult.classList.add('error-message');
    }


    function disableProcessingSaving() {
      const saveButton = document.getElementById('save-button');
      saveButton.textContent = saveButton.dataset.defaultValue;
      saveButton.disabled = false;

      document.getElementById('loader').hidden = true;
    }

    /**
     * Copy button handler.
     */
    function copyButtonListener() {
      let copyBtn = document.getElementById('copy-button');
      copyBtn.addEventListener('click', (event) => {
        event.preventDefault();
        copyURLToClipboard(event);
      });

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
      function copyURLToClipboard(event) {
        let url = document.getElementById('url-result');
        url.value = window.location.origin + url.dataset.location;
        url.hidden = false;
        url.select();
        document.execCommand('copy');
        url.hidden = true;

        event.target.dataset.defaultValue = event.target.textContent;
        event.target.textContent = 'URL copied';
        event.target.disabled = true;

        setTimeout(() => {
          event.target.textContent = event.target.dataset.defaultValue;
          event.target.disabled = false;
        }, 2000);
      }
    }
  }
)
;
