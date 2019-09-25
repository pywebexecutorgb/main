<template>
  <div class="block">
    <h4 class="block-header">Confirm email</h4>
    <p id="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "UserValidateEmail",
  props: ["uid", "token"],

  data() {
    return {
      message: "No result",

      // imported methods
      getURL: methods.getURL,
      getJSON: methods.getJSON,
      showElementMessageClass: methods.showElementMessageClass
    };
  },

  methods: {
    showError(message) {
      return this.showElementMessageClass("message", message, "error");
    },

    showSuccess(message) {
      this.showElementMessageClass(
        "message",
        `${message} Redirect after 5 seconds.`,
        "successful"
      );
      return setTimeout(() => this.$router.push({ path: "/" }), 5000);
    },

    async checkVerificationToken() {
      const url = this.getURL("validateEmail", `${this.uid}/${this.token}`);

      await this.getJSON(url, {
        credentials: "include"
      })
        .then(response => {
          if (response.hasOwnProperty("error")) {
            return this.showError(response.error);
          }
          this.$parent.$refs.login.getUserInfo();
          this.showSuccess("Email verified.");
        })
        .catch(error => this.showError(error));
    }
  },

  mounted() {
    this.checkVerificationToken();
  }
};
</script>

<style scoped>
.block {
  display: flex;
  flex-direction: column;
}

.block-header {
  text-align: center;
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

.error {
  color: red;
  border-color: orangered;
}

.successful {
  color: green;
  border-color: mediumseagreen;
}
</style>