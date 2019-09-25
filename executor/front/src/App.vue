<template>
  <div id="app" class="container">
    <header>
      <router-link class="header-title" to="/">py exec</router-link>
      <user-login ref="login"></user-login>
    </header>

    <div class="top">
      <keep-alive>
        <router-view :key="$route.fullPath"></router-view>
      </keep-alive>
    </div>
    <footer class="site-footer">
      <a href="https://github.com/pywebexecutorgb">web executor</a> &copy;&nbsp;2019
    </footer>
  </div>
</template>

<script>
import methods from "./methods.js";
import UserLogin from "./components/UserLogin.vue";

export default {
  name: "app",

  data() {
    return {
      // imported methods
      getURL: methods.getURL,
      getJSON: methods.getJSON,
      getCookie: methods.getCookie
    };
  },

  components: {
    UserLogin
  },

  created() {
    this.createContainer();
    window.addEventListener("unload", this.deleteContainer);
  },

  mounted() {
    setInterval(this.sendHealthCheck, 10000);
  },

  methods: {
    /**
     * Function create container on created Vue add:
     * make POST request to REST API
     */
    createContainer() {
      if (this.$store.getters.getContainer) {
        return true;
      }

      const csrfToken = this.getCookie("csrftoken");
      this.getJSON(this.getURL("createContainer"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(data => this.$store.commit("setContainer", data["container_id"]))
        .catch(error =>
          this.$store.commit(
            "setError",
            `Cannot create init container: ${error.message}`
          )
        );
    },

    /**
     * Remove container on beforeunload action.
     */
    deleteContainer() {
      const containerID = this.$store.getters.getContainer;
      if (!containerID) {
        return false;
      }

      const csrfToken = this.getCookie("csrftoken");
      fetch(this.getURL("changeContainer", containerID), {
        method: "DELETE",
        headers: {
          "X-CSRFToken": csrfToken
        }
      });

      this.$store.commit("setContainer", null);
    },

    /**
     * Function send PUT request in timeout interval,
     * by timestamp value we removed unused containers on backend side.
     */
    sendHealthCheck() {
      const containerID = this.$store.getters.getContainer;
      if (!containerID) {
        return false;
      }

      const csrfToken = this.getCookie("csrftoken");
      fetch(this.getURL("changeContainer", containerID), {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ date: Date.now() })
      })
        .then(response => {
          if (response.status !== 204) {
            throw new Error("received wrong status code");
          }
          this.$store.commit("setError", null);
        })
        .catch(error =>
          this.$store.commit(
            "setError",
            `Error while send container health check, please refresh page. Detail: "${error.message}"`
          )
        );
    }
  }
};
</script>

<style scoped>
header,
footer {
  margin: 5px 0 5px;
  padding: 0 5px;
  height: 45px;
  background-color: #424242;
  color: whitesmoke;
  border-radius: 5px;

  align-items: center;

  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

header {
  display: flex !important;
  flex-direction: row;
  justify-content: space-between;

  padding-left: 15px;
}

footer {
  padding-right: 15px;
  text-align: right;

  line-height: 45px;
  text-transform: uppercase;
}

.header-title:any-link {
  display: block;
  color: unset;
  text-transform: uppercase;
}

.site-footer:any-link,
.site-footer a:any-link {
  color: unset;
}

.container {
  margin: 0 auto;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.top {
  flex-grow: 1;
}
</style>
