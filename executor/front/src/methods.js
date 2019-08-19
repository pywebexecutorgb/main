export default {
  name: "methods",

  /**
   * Function make URL request and parse JSON answer
   * @param url, string
   * @param params, fetch {Object}
   * @return {Promise}, fetch promise
   */
  getJSON(url, params = {}) {
    return fetch(url, params)
      .then(response => response.json())
      // eslint-disable-next-line no-console
      .catch(error => console.log(error))
  },

  /**
   * URL API logic: return URL string by input params.
   * @param name, {string} - action name
   * @param param, {string} - param is container ID
   * @return url, {string}
   */
  getURL(name, param = null) {
    switch (name) {
      // code API
      case "createContainer":
        return "http://localhost:8000/api/containers/";
      case "saveCode":
        return "http://localhost:8000/api/code-bases/";
      case "execCode":
        return `http://localhost:8000/api/containers/${param}/codes/`;
      case "readCode":
        return `http://localhost:8000/api/code-executions/${param}/`;
      case "changeContainer":
        return `http://localhost:8000/api/containers/${param}/`;

      // user API
      case "createUser":
        return "http://localhost:8000/api/users/";
      case "showUser":
        return "http://localhost:8000/api/users/";
      case "deleteUser":
        return `http://localhost:8000/api/users/${param}`;
      case "loginUser":
        return "http://localhost:8000/api/auth/";
      case "logoutUser":
        return "http://localhost:8000/api/auth/";
      case "profileUser":
        return "http://localhost:8000/api/user/profile/";
      case "historyUser":
        return "http://localhost:8000/api/history/";
      case "validateEmail":
        return `http://localhost:8000/api/auth/validate-email/${param}/`;
      case "initResetPasswordUser":
        return "http://localhost:8000/api/auth/reset-password/";
      case "ResetPasswordUser":
        return `http://localhost:8000/api/auth/reset-password/${param}/`;

      // short URL
      case "shortURL":
        return `http://localhost:8000/api/short-url/${param}`;
    }
  },

  /**
   * Function parse Cookie header and get value by name
   * @param {string}, cookie key name
   * @return {string}, cookie value
   */
  getCookie(key) {
    const regexp = new RegExp(`${key}=([^;]+)`);
    const value = regexp.exec(document.cookie);

    if (value === null) {
      return '';
    }
    return value[1];
  },

  /**
   * Function reset data values
   */
  resetInitData() {
    Object.assign(this.$data, this.$options.data.apply(this));
  },

  /**
   * Update data values with input object — assign
   * @param {Object}, valuesObject
   */
  setValues(valuesObject) {
    Object.assign(this, valuesObject);
  },

  /**
   * Function make redirect with next call,
   *   where next is router-redirect input object.
   * @param hash, Code ID, presented in short format
   * @param next, router-redirect BeforeStart object
   */
  nextShortURL(hash, next) {
    this.getJSON(this.getURL('shortURL', hash))
      .then(response => {
        if (response.hasOwnProperty('code_id')) {
          return next(`/code/${response.code_id}`);
        }
        return next('/');
      })
      .catch(() => next('/'));
  },

  /**
   * Function make block unhidden and add message with class to block.
   * @param elementID, string
   * @param message, string
   * @param customClass, string
   * @returns {boolean}, false if block was not found
   */
  showElementMessageClass(elementID, message = '', customClass = null) {
    const element = document.getElementById(elementID);
    if (!element) {
      return false;
    }

    element.hidden = false;
    if (message)
      element.textContent = message;
    if (customClass)
      element.classList.add(customClass);

    return true;
  },

  /**
   * Function make block hidden and remove message with class from block.
   * @param elementID, string
   * @param customClass, string
   * @returns {boolean}, false if block was not found
   */
  hideElementClass(elementID, customClass = null) {
    const element = document.getElementById(elementID);
    element.hidden = false;
    element.textContent = null;

    if (customClass)
      element.classList.remove(customClass);
    return true;
  },

  /**
   * Function check value with regexp by value type,
   * like a pssword, username, etc
   * @param value, string, that need to check
   * @param type, string
   * @returns {boolean}
   */
  isValidValue(value, type) {
    const regexp = {
      'username': new RegExp("^[-\\w]+$", "i"),
      'email': new RegExp("^[-\\w]+@[-\\w]+\\.[-\\w]+(\\.[-\\w]+)*$", "i"),
      'password': new RegExp("^.{4,}$", "i"),
    };

    if (!regexp.hasOwnProperty(type)) {
      return false;
    }

    return regexp[type].test(value);
  },

  /**
   * Function return error message for current field type,
   *   it's using when user input wrong values
   * @param type, string
   * @returns {string}
   */
  getErrorMessage(type) {
    const errorMessage = {
      'username': 'Username must contains word, numbers and _, -',
      'email': 'Email must contains login, @ and domain',
      'password': 'Password must contains minimum 4 characters',
    };

    if (!errorMessage.hasOwnProperty(type)) {
      return 'Undefined error for current field';
    }

    return errorMessage[type];
  },
};
