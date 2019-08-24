import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    user: null,
    error: null,
    container: null,
  },

  mutations: {
    setError: (state, message) => state.error = message,
    setUser: (state, userDescription) => state.user = userDescription,
    setContainer: (state, containerID) => state.container = containerID,
  },

  getters: {
    getError: state => state.error,
    getUser: state => state.user,
    getContainer: state => state.container,
  }
});