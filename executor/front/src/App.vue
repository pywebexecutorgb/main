<template>
    <div id="app" class="container">
        <header>
            <router-link class="header-title" to="/">py exec</router-link>
            <user-login ref="login"></user-login>
        </header>

        <div class="top">
            <router-view></router-view>
        </div>
        <footer class="site-footer">
            <a href="https://github.com/pywebexecutorgb">web executor</a> &copy;&nbsp;2019
        </footer>
    </div>
</template>

<script>
  import UserLogin from './components/UserLogin.vue';

  export default {
    name: 'app',

    components: {
      UserLogin,
    },
  }
</script>

<style scoped>
    header, footer {
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
