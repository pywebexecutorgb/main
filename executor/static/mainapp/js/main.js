"use strict";

window.addEventListener('load', () => {
  clearButtonListener();
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
      url.value = url.dataset.domain + url.dataset.location;
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
});
