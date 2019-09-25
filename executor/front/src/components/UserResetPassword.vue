<template>
  <div class="reset-password-form">
    <h4 class="block-header">Reset password</h4>

    <div class="input-form">
      <div class="input-group mb-1">
        <div class="input-group-prepend">
          <span class="icon-input input-group-text" id="password-addon">&#128273;</span>
        </div>
        <input
          id="passwordNew"
          type="password"
          class="form-control"
          placeholder="password"
          v-model="passwordNew"
          aria-describedby="password-addon"
          data-type="password"
          @change="isValidPassword()"
        />
      </div>
    </div>

    <div class="input-form">
      <div class="input-group mb-1">
        <div class="input-group-prepend">
          <span class="icon-input input-group-text" id="password-confirm-addon">&#128273;</span>
        </div>
        <input
          id="passwordNewConfirm"
          type="password"
          class="form-control"
          placeholder="confirm password"
          v-model="passwordNewConfirm"
          aria-describedby="password-confirm-addon"
          data-type="password"
          @change="isValidPassword()"
        />
      </div>
    </div>

    <div class="reset-password-buttons">
      <button
        @click="resetPassword()"
        class="reset-password-button btn btn-outline-success"
      >Reset password</button>
      <button
        @click="resetInitData()"
        type="reset"
        class="reset-password-button btn btn-outline-danger"
      >Clear</button>
    </div>

    <div id="error-reset-password" class="error-reset-password" hidden></div>
  </div>
</template>

<script>
// CLEAN REPEATED BLOCKS with UserCreate
import methods from "../methods.js";

export default {
  name: "UserResetPassword",
  props: ["uid", "token"],

  data() {
    return {
      passwordNew: "",
      passwordNewConfirm: "",

      // imported methods
      getURL: methods.getURL,
      getJSON: methods.getJSON,
      resetInitData: methods.resetInitData,

      showElementMessageClass: methods.showElementMessageClass,
      hideElementClass: methods.hideElementClass,
      isValidValue: methods.isValidValue,
      getErrorMessage: methods.getErrorMessage
    };
  },

  methods: {
    showError(message) {
      return this.showElementMessageClass("error-reset-password", message);
    },

    showSuccess(message) {
      this.showElementMessageClass(
        "error-reset-password",
        `${message} Redirect after 5 seconds.`,
        "successful"
      );
      return setTimeout(() => this.$router.push({ path: "/" }), 5000);
    },

    hideError() {
      return this.hideElementClass("error-reset-password");
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

    isValidPassword() {
      if (this.passwordNew !== this.passwordNewConfirm) {
        document.getElementById("passwordNew").classList.add("error-input");
        document
          .getElementById("passwordNewConfirm")
          .classList.add("error-input");
        this.showError("Passwords are not equal");
        return false;
      }

      document.getElementById("passwordNew").classList.remove("error-input");
      document
        .getElementById("passwordNewConfirm")
        .classList.remove("error-input");
      this.hideError();

      return this.isValidInput("passwordNew");
    },

    resetPassword() {
      if (!this.isValidPassword()) {
        return false;
      }

      const url = this.getURL("ResetPasswordUser", `${this.uid}/${this.token}`);
      const body = JSON.stringify({
        password: this.passwordNew
      });

      this.getJSON(url, {
        body,
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
        .then(response => {
          if (response.hasOwnProperty("error")) {
            return this.showError(response.error);
          }
          return this.showSuccess("Password has been changed.");
        })
        .catch(error => this.showError(error));
    }
  }
};
</script>

<style scoped>
@media screen and (max-width: 768px) {
  .btn {
    width: 48% !important;
    margin-right: unset !important;
  }
}

.icon-input {
  width: 40px !important;
}

.error-reset-password {
  color: orangered;
  font-weight: 200;
  text-align: center;
}

.block-header {
  text-align: center;
}

.reset-password-form {
  margin: 20px auto;
  display: flex;
  flex-direction: column;

  width: 50%;
  min-width: 250px;
}

.reset-password-buttons {
  display: flex;
  width: 100% !important;
  justify-content: space-around;
}

.reset-password-button {
  margin: 10px 0;
  width: 30% !important;
  min-width: 100px;
}

.successful {
  color: green !important;
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
