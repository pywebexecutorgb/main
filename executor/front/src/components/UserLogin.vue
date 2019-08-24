<template>
    <div class="header-menu">
        <img class="user-picture" src="/img/user.svg" alt="pic" @click="showLogin = !showLogin">
        <div v-show="showLogin" class="user-profile">
            <!-- user logged in -->
            <div v-if="user">
                <ul>
                    <li>
                        <router-link class="header-title" to="/user/history">History</router-link>
                    </li>
                    <li>
                        <router-link class="header-title" to="/user/profile">Profile</router-link>
                    </li>
                    <li>
                        <button @click="logoutUser" class="user-buttons btn btn-outline-danger">Logout</button>
                    </li>
                </ul>
            </div>

            <!-- anonymous user -->
            <div v-else>
                <ul>
                    <li>
                        <div class="input-group mb-1">
                            <div class="input-group-prepend">
                                <span class="icon-input input-group-text" id="eauth-email-addon">@</span>
                            </div>
                            <input id="authEmail" type="text" class="form-control" placeholder="email"
                                   v-model="authEmail" aria-describedby="auth-email-addon" data-type="email"
                                   @change="isValidInput('authEmail')">
                        </div>
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <span class="icon-input input-group-text" id="auth-password-addon">&#128273;</span>
                            </div>
                            <input id="authPassword" type="password" class="form-control" placeholder="password"
                                   v-model="authPassword" aria-describedby="auth-password-addon" data-type="password"
                                   @change="isValidInput('authPassword')">
                        </div>
                    </li>
                    <li>
                        <router-link class="header-title" to="/user/create">Sign up</router-link>
                    </li>
                    <li>
                        <button @click="loginUser()"
                                class="user-buttons btn btn-outline-success">Login
                        </button>
                    </li>
                    <li>
                        <button @click="resetPasswordUser()"
                                class="user-buttons btn btn-outline-secondary">Reset password
                        </button>
                    </li>
                    <li>
                        <div id="error-login" class="error-login" hidden></div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
  import methods from '../methods.js';

  export default {
    name: "UserLogin",

    data() {
      return {
        showLogin: false,

        // authorized main data
        authEmail: '',
        authPassword: '',

        // imported methods
        getURL: methods.getURL,
        getJSON: methods.getJSON,
        getCookie: methods.getCookie,

        showElementMessageClass: methods.showElementMessageClass,
        hideElementClass: methods.hideElementClass,
        isValidValue: methods.isValidValue,
        getErrorMessage: methods.getErrorMessage,
      }
    },

    computed: {
      user() {
        return this.$store.getters.getUser;
      }
    },

    created() {
      this.getUserInfo();
    },

    methods: {
      showError(message) {
        return this.showElementMessageClass('error-login', message);
      },

      hideError() {
        return this.hideElementClass('error-login');
      },

      /**
       * Function update user data variable throw API.
       */
      getUserInfo() {
        const url = this.getURL('showUser');
        this.getJSON(url, {credentials: 'include'})
          .then(response => {
            if (response.hasOwnProperty('error')) {
              this.$store.commit('setUser', null);
              // eslint-disable-next-line no-console
              console.log(`Fetch user data error: ${response.error}`);
            } else {
              this.$store.commit('setUser', response);
            }
          });
      },

      async loginUser() {
        if (!this.isValidInput("authEmail") || !this.isValidInput("authPassword")) {
          return false;
        }

        const url = this.getURL('loginUser');
        const csrfToken = this.getCookie('csrftoken');
        const body = JSON.stringify({
          'email': this.authEmail,
          'password': this.authPassword,
        });

        await this.getJSON(url, {
          credentials: 'include',
          body,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
        });
        this.getUserInfo();

        if (!this.$store.getters.getUser) {
          this.showError('Login incorrect');
        }
      },

      async logoutUser() {
        const url = this.getURL('logoutUser');
        const csrfToken = this.getCookie('csrftoken');

        await this.getJSON(url, {
          credentials: 'include',
          method: 'DELETE',
          headers: {'X-CSRFToken': csrfToken}
        });
        this.getUserInfo();
      },

      async resetPasswordUser() {
        if (!this.isValidInput("authEmail")) {
          return false;
        }

        const url = this.getURL('initResetPasswordUser');
        const csrfToken = this.getCookie('csrftoken');
        const body = JSON.stringify({
          'email': this.authEmail,
        });

        await this.getJSON(url, {
          credentials: 'include',
          body,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
        })
          .then(response => {
            if (response.hasOwnProperty('error')) {
              return this.showError(response.error)
            }
            return this.showError("Check your email and follow the link");
          })
          .catch(error => this.showError(error));
      },

      isValidInput(fieldName) {
        const el = document.getElementById(fieldName);
        const elType = el.dataset.type;
        if (!this.isValidValue(this[fieldName], elType)) {
          el.classList.add("error-input");
          this.showError(this.getErrorMessage(elType));
          return false;
        }

        el.classList.remove("error-input");
        this.hideError();
        return true;
      },
    },
  }
</script>

<style scoped>
    .header-title:any-link {
        display: block;
        color: unset;
        text-transform: uppercase;
    }

    .header-menu {
        position: relative;
    }

    .user-profile {
        position: absolute;
        z-index: 1;
        top: 42px;
        right: 0px;

        border-radius: 5px;
        border: 1px solid whitesmoke;
        background-color: #424242;

        padding: 5px;
        width: 250px;

        text-align: center;
    }

    .user-picture {
        border-radius: 3px;
        background-color: white;
        padding: 1px;
        width: 35px;
        height: 35px;
    }

    .user-profile li {
        list-style: none;
    }

    .user-profile ul {
        margin: 0px !important;
    }

    .user-buttons {
        width: 100% !important;
    }

    .icon-input {
        width: 40px !important;
    }

    .error-login {
        color: orangered;
        font-weight: 200;
        text-align: center;
    }

    .error-input {
        border: 2px solid orangered !important;
    }

    .btn {
        width: 130px;
        margin-top: 10px;
        margin-right: 5px;
    }

    .btn:last-child {
        margin-right: 0;
    }
</style>