import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    user: null,
    error: null,
  },

  mutations: {
    setError: (state, message) => {
      state.error = message;
    },
    setUser: (state, userDescription) => {
      state.user = userDescription;
    },
  },

  getters: {
    getError: state => {
      return state.error;
    },
    getUser: state => {
      return state.user;
    },
  }
});