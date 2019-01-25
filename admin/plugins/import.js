import Vue from 'vue';
import VeeValidate from 'vee-validate';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import _ from 'lodash';
import colors from 'vuetify/es5/util/colors';
import InstantSearch from 'vue-instantsearch';
import {Howl, Howler} from 'howler';

// Not Working here but will probably work in next versions
// It's due to SSR and Vuetify recompiling itself with window or something
Vue.use(Vuetify, {
  theme: {
    primary: colors.blue.darken2,
    secondary: colors.blue.darken1,
    accent: colors.blue.accent4,
    warning: colors.orange.darken4,
    info: colors.blue.darken4,
    success: colors.green.darken4,
    error: colors.red.accent4
  }
});

Vue.use(InstantSearch);
Vue.set(Vue.prototype, '_', _);
Vue.prototype.$eventHub = new Vue();
Vue.use(VeeValidate);

export const EventBus = new Vue();