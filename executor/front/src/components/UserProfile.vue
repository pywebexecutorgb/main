<template>
    <div class="block">
        <h4 class="block-header">Update user profile</h4>
        <div v-if="user" class="user-form-block">
            <form v-if="form" id="user-form">
                <div v-html="form"></div>
                <div class="user-form-buttons">
                    <button @click.prevent="submit()" class="user-form-button btn btn-outline-success">
                        Save
                    </button>
                    <button type="reset" class="user-form-button btn btn-outline-danger">Clear</button>
                </div>
            </form>
            <!-- form fetch error -->
            <div v-else class="message error-submit">{{fetchFormMessage}}</div>

            <div id="error-submit" class="error-submit" hidden></div>
        </div>
        <div v-else class="message error-submit">
            You must be logged in.
        </div>
    </div>
</template>

<script>
  import methods from '../methods.js';

  export default {
    name: "UserProfile",

    data() {
      return {
        form: null,
        fetchFormMessage: 'Waiting for form loading.',

        // imported methods
        getURL: methods.getURL,
        getJSON: methods.getJSON,
        showElementMessageClass: methods.showElementMessageClass,
        hideElementClass: methods.hideElementClass,
      }
    },

    computed: {
      user() {
        return this.$store.getters.getUser;
      },
    },

    watch: {
      user() {
        this.getProfileForm()
      },
    },

    mounted() {
      this.getProfileForm();
    },

    methods: {
      showError(message) {
        return this.showElementMessageClass("error-submit", message);
      },

      showSuccess(message) {
        this.showElementMessageClass("error-submit", message, "successful");
      },

      hideError() {
        return this.hideElementClass("error-submit", "successful");
      },

      /**
       * Function update user data variable throw API.
       */
      getProfileForm() {
        const url = this.getURL('profileUser');
        fetch(url, {credentials: 'include'})
          .then(response => response.text())
          .then(response => {
            if (response.hasOwnProperty('error')) {
              this.fetchFormMessage = `Fetch user data error: ${response.error}`;
            } else {
              this.form = response;
            }
          })
          .catch(error => this.fetchFormMessage = error);
      },

      submit() {
        this.hideError();
        const body = new FormData(document.getElementById("user-form"));

        this.getJSON(this.getURL('profileUser'), {
          credentials: 'include',
          body,
          method: 'POST',
        })
          .then(response => {
            if (response.hasOwnProperty("error")) {
              return this.showError(response.error)
            }
            return this.showSuccess("Profile has been updated.");
          })
          .catch(error => this.showError(error));
      },
    },
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        .user-form-block {
            width: 100% !important;
        }
    }

    .block {
        display: flex;
        flex-direction: column;
    }

    .block-header {
        text-align: center;
    }

    .user-form-block {
        margin: 20px auto;
        display: flex;
        flex-direction: column;

        width: 50%;
        min-width: 250px;
    }

    .user-form-buttons {
        display: flex;
        width: 100% !important;
        justify-content: space-around;
    }

    .user-form-button {
        margin: 10px 0;
        width: 30% !important;
        min-width: 100px;
    }

    .message {
        display: inline;
        border: 1px solid;
        border-radius: 3px;

        max-width: 400px;
        min-height: 50px;
        text-align: center;

        align-self: center;
        font-size: large;

        padding: 10px 15px;
    }

    .error-submit {
        color: orangered;
        font-weight: 200;
        text-align: center;
    }

    .successful {
        color: green !important;
    }
</style>
