<template>
    <div class="block">
        <h4 class="block-header">User history</h4>
        <div v-if="user" class="user-history-block">
            <div v-if="isHistoryCount">
                <table class="history-block table table-striped table-dark">
                    <colgroup>
                        <col class="link"/>
                        <col class="code"/>
                        <col class="dependencies"/>
                        <col class="date"/>
                    </colgroup>
                    <thead class="thead-dark">
                    <tr>
                        <th scope="col"></th>
                        <th scope="col">Code</th>
                        <th scope="col">Dependencies</th>
                        <th scope="col">Created at</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="raw in history.results">
                        <td>
                            <router-link class="link-href" :to="getCodeLinkById(raw.code.pk)">&ogt;</router-link>
                        </td>
                        <td class="align-middle">
                            <pre>{{raw.code.code_text}}</pre>
                        </td>
                        <td class="align-middle">
                            <pre>{{raw.code.dependencies}}</pre>
                        </td>
                        <td class="align-middle">
                            <pre>{{raw.code.created_at}}</pre>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <div class="buttons btn-group" role="group">
                    <button type="button" class="btn btn-outline-secondary" :disabled="!history.previous"
                            @click="getUserHistory(history.previous)">Prev
                    </button>
                    <button type="button" class="btn btn-outline-secondary" :disabled="!history.next"
                            @click="getUserHistory(history.next)">Next
                    </button>
                </div>
            </div>

            <!-- form history error -->
            <div v-else class="message error">{{fetchHistoryMessage}}</div>
        </div>

        <!-- when user is not defined -->
        <div v-else class="message error">
            You must be logged in.
        </div>
    </div>
</template>

<script>
  import methods from '../methods.js';

  export default {
    name: "UserHistory",

    data() {
      return {
        history: null,
        fetchHistoryMessage: 'Waiting for history loading.',

        // imported methods
        getURL: methods.getURL,
        getJSON: methods.getJSON,
      }
    },

    computed: {
      user() {
        return this.$store.getters.getUser;
      },
      isHistoryCount() {
        return this.history && this.history.hasOwnProperty('count') && this.history.count > 0;
      },
    },

    watch: {
      user() {
        this.getUserHistory()
      },
    },

    mounted() {
      this.getUserHistory();
    },

    methods: {
      getCodeLinkById(id) {
        return `/code/${id}`;
      },

      getUserHistory(url = null) {
        if (!url) {
          url = this.getURL('historyUser');
        }

        this.getJSON(url, {
          credentials: 'include',
        })
          .then(response => {
            if (response.hasOwnProperty("error")) {
              return this.fetchHistoryMessage = response.error;
            }
            this.fetchHistoryMessage = 'Form has been fetched.';
            this.history = response;
          })
          .catch(error => this.fetchHistoryMessage = error);
      },
    }
  }
</script>

<style scoped>
    @media screen and (max-width: 768px) {
        th {
            display: none;
        }

        td, col {
            display: block;
        }

        .link-href {
            display: block;
            text-align: center;
        }
    }

    .block {
        display: flex;
        flex-direction: column;
    }

    .block-header {
        text-align: center;
    }

    .user-history-block {
        display: flex;
        justify-content: center;
    }

    table {
        width: 100%;
        table-layout: fixed;
    }

    pre {
        color: lightgray;
        overflow: hidden;
        margin-bottom: 0;
    }

    .link {
        width: 3%;
        overflow: hidden;
    }

    .link-href {
        text-decoration: underline;
        color: white;
        font-size: 24px;
    }

    .code {
        width: 40%;
        overflow: hidden;
    }

    .dependencies {
        width: 30%;
        overflow: hidden;
    }

    .date {
        width: 27%;
        overflow: hidden;
    }

    .buttons {
        display: block;
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
        color: orangered;
        font-weight: 200;
        text-align: center;
    }
</style>