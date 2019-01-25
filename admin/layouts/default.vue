<template>
    <v-app class="grey lighten-4">
        <v-toolbar fixed style="height: 19vh">
            <v-toolbar-side-icon v-show="isAdmin" @click="drawer = true"></v-toolbar-side-icon>
            <v-toolbar-title>
                <img class="mt-5" width="300" :src="imageUrlFormated('ze.png')"/>
            </v-toolbar-title>
            <v-toolbar-items>
                <template v-show='!this.$store.state.user.loading'>
                    <v-btn flat v-if="!logged" @click="dialog = true">Login</v-btn>
                    <v-btn flat v-else @click="logout()">Logout</v-btn>
                </template>
            </v-toolbar-items>
        </v-toolbar>
        <v-navigation-drawer
            v-model="drawer"
            v-show="isAdmin"
            absolute
            temporary
            floating>
            <v-list class="pt-0" dense>
                <v-divider></v-divider>
                <div v-if="$store.state.dbStruct">
                    <v-list-tile>
                        <v-list-tile-content class="display-1 mt-3 ml-3">
                            Admin Pannel
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider class="my-3"/>
                    <v-list-tile v-for="(item, index) in $store.state.dbStruct" :key="item + index">
                        <v-list-tile-content class="subheading ml-3">
                            <nuxt-link :to="'/' + index" @click.native="drawer = false">
                                {{ index | startCase}}
                            </nuxt-link>
                        </v-list-tile-content>
                    </v-list-tile>
                </div>
            </v-list>
            <LoginComponent :dialog="dialog" @closeDialog="dialog = false"/>
        </v-navigation-drawer>
        <v-container fluid align-content-start style="margin-top: 135px;" class="grey lighten-2">
            <nuxt/>
            <TooltipComponent/>
        </v-container>
    </v-app>
</template>
<script>
import LoginComponent from '@/components/login/LoginComponent.vue';
import TooltipComponent from '@/components/TooltipComponent.vue';

export default {
    data() {
        return {
            dialog: false,
            drawer: false,
        }
    },
    components: {
        LoginComponent,
        TooltipComponent
    },
    created() {
        this.$vuetify.theme.primary = "#002e5b";
        this.$vuetify.theme.secondary = "#00f0a4";
        this.$vuetify.theme.accent = "#B71C1C";
        this.$vuetify.theme.error = "#D50000";
        this.$vuetify.theme.warning = "#E65100";
        this.$vuetify.theme.info = "#0D47A1";
        this.$vuetify.theme.success = "#1B5E20";
    },
    beforeCreate() {
        this.$store.commit('initialiseStore');
    },
    destroyed() {
        this.$root.$off('refresh', this.force_refresh);
    },
    computed: {
        route: {
            get: function () {
                console.log(this.$route.path);
              return this.$route.path;
            },
            set: function (newValue) {
            }
        },
        logged() {
            if (this.$store.state.user.auth_token == null
                || this.$store.state.user.auth_token == '') {
                return false;
            }
            return true;
        },
        isAdmin: function() {
            return this.$store.state.user.admin
        },
    },
    methods: {
        imageUrlFormated: function(value) {
            var img;
            try {
                img = require('@/static/img/' + value);
            }
            catch (error) {
                console.log("⚠️ 📸 Image not found :", error);
                img = require('@/static/img/ze.png');
            }
            return img;
        },
    }
};
</script>


<style scoped>
.v-dialog__content.v-dialog__content--active {
    background-color: rgba(0, 0, 0, 0.4);
}
</style>
<style>
body .application.theme--dark {
    background-image: url('http://0.0.0.0:3000/img/main/fond_rouge_flou.jpg');
    color: #fff;
    background-repeat: repeat;
    background-size: 101%;
    background-position: 0px 90px;
    background-attachment: fixed;
}
.v-toolbar__title {
    width: 100%;
}
.v-toolbar__title span {
    margin: auto;
    display: block;
    width: fit-content;
    font-size: 2.5em;
}
html {
    font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 16px;
    word-spacing: 1px;
    -ms-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    box-sizing: border-box;
}
*,
*:before,
*:after {
    box-sizing: border-box;
    margin: 0;
}
.button--green {
    display: inline-block;
    border-radius: 4px;
    border: 1px solid #3b8070;
    color: #3b8070;
    text-decoration: none;
    padding: 10px 30px;
}
.button--green:hover {
    color: #fff;
    background-color: #3b8070;
}
.button--grey {
    display: inline-block;
    border-radius: 4px;
    border: 1px solid #35495e;
    color: #35495e;
    text-decoration: none;
    padding: 10px 30px;
    margin-left: 15px;
}
.button--grey:hover {
    color: #fff;
    background-color: #35495e;
}
</style>
