<template>
    <div class="create-user-form">
        <h4 class="block-header">Sign up</h4>
        <div class="input-form">
            <div class="input-group mb-1">
                <div class="input-group-prepend">
                    <span class="icon-input input-group-text" id="email-addon">@</span>
                </div>
                <input id="email" type="text" class="form-control" placeholder="email"
                       v-model="email" aria-describedby="email-addon" @change="isValidInput('email')">
            </div>
        </div>

        <div class="input-form">
            <div class="input-group mb-1">
                <div class="input-group-prepend">
                    <span class="icon-input input-group-text" id="username-addon">&#128100;</span>
                </div>
                <input id="username" type="text" class="form-control" placeholder="username"
                       v-model="username" aria-describedby="username-addon"
                       @change="isValidInput('username')">
            </div>
        </div>

        <div class="input-form">
            <div class="input-group mb-1">
                <div class="input-group-prepend">
                    <span class="icon-input input-group-text" id="password-addon">&#128273;</span>
                </div>
                <input id="password" type="text" class="form-control" placeholder="password"
                       v-model="password" aria-describedby="password-addon" @change="isValidPassword()">
            </div>
        </div>

        <div class="input-form">
            <div class="input-group mb-1">
                <div class="input-group-prepend">
                    <span class="icon-input input-group-text" id="password-confirm-addon">&#128273;</span>
                </div>
                <input id="passwordConfirm" type="text" class="form-control"
                       placeholder="confirm password"
                       v-model="passwordConfirm" aria-describedby="password-confirm-addon"
                       @change="isValidPassword()">
            </div>
        </div>

        <div class="create-user-buttons">
            <button @click="create()"
                    class="create-user-button btn btn-outline-success">Sign up
            </button>
            <button @click="resetInitData()" type="reset"
                    class="create-user-button btn btn-outline-danger">Clear
            </button>
        </div>

        <div id="error-create" class="error-create" hidden></div>
    </div>
</template>

<script>
  import methods from '../methods.js';

  export default {
    name: "CreateUser",

    data() {
      return {
        username: '',
        email: '',
        password: '',
        passwordConfirm: '',

        // imported methods
        getURL: methods.getURL,
        getJSON: methods.getJSON,
        resetInitData: methods.resetInitData,

        showElementMessageClass: methods.showElementMessageClass,
        hideElementClass: methods.hideElementClass,
        isValidValue: methods.isValidValue,
        getErrorMessage: methods.getErrorMessage,
      };
    },

    methods: {
      showError(message) {
        return this.showElementMessageClass('error-create', message);
      },

      hideError() {
        return this.hideElementClass('error-create');
      },

      isValidInput(fieldName) {
        const el = document.getElementById(fieldName);
        if (!this.isValidValue(this[fieldName], fieldName)) {
          el.classList.add("error-input");
          this.showError(this.getErrorMessage(fieldName));
          return false;
        }

        el.classList.remove("error-input");
        this.hideError();
        return true;
      },

      isValidPassword() {
        if (this.password !== this.passwordConfirm) {
          document.getElementById('password').classList.add("error-input");
          document.getElementById('passwordConfirm').classList.add("error-input");

          this.showError('Passwords are not equal');
          return false;
        }

        document.getElementById('password').classList.remove("error-input");
        document.getElementById('passwordConfirm').classList.remove("error-input");
        this.hideError();

        return this.isValidInput('password');
      },

      create() {
        if (!this.isValidInput("email")
          || !this.isValidInput("username")
          || !this.isValidPassword()) {
          return false;
        }

        const url = this.getURL('createUser');
        const body = JSON.stringify({
          'username': this.username,
          'email': this.email,
          'password': this.password,
        });

        this.getJSON(url, {
          body,
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
        })
          .then(response => {
            if (response.hasOwnProperty('id')) {
              this.showError("Check your email and validate user by link.")
            } else {
              this.showError(JSON.stringify(response.error));
            }
          });
      },
    },
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        .create-user-form {
            width: 100% !important;
        }

        .btn {
            width: 48% !important;
            margin-right: unset !important;
        }
    }

    .icon-input {
        width: 40px !important;
    }

    .error-create {
        color: orangered;
        font-weight: 200;
        text-align: center;
    }

    .block-header {
        text-align: center;
    }

    .create-user-form {
        margin: 20px auto;
        display: flex;
        flex-direction: column;

        width: 50%;
        min-width: 250px;
    }

    .create-user-buttons {
        display: flex;
        width: 100% !important;
        justify-content: space-around;
    }

    .create-user-button {
        margin: 10px 0;
        width: 30% !important;
        min-width: 100px;
    }

    .input-form {
        /* profile button use is */
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .btn {
        width: 130px;
        margin-top: 10px;
        margin-right: 5px;
    }

    .btn:last-child {
        margin-right: 0;
    }

    .error-input {
        border: 2px solid orangered !important;
    }
</style>
