<template>
    <section class="container">
        <v-layout v-if="success == false">
            <div>
                Set your password to access you acount, and everything will be great !
            </div>
            <form>
                <v-text-field
                    v-validate="'required'"
                    v-model="password"
                    ref="password"
                    :error-messages="errors.collect('password')"
                    label="Password"
                    data-vv-name="password"
                    type="password"
                    required>
                </v-text-field>
                <v-text-field
                    v-validate="{required: true, is: password}"
                    v-model="passwordConfirm"
                    :error-messages="errors.collect('passwordConfirm')"
                    label="Password confirmation"
                    data-vv-name="passwordConfirm"
                    ref="passwordConfirm"
                    type="password"
                    required>
                </v-text-field>
                <v-btn @click="submit">submit</v-btn>
            </form>
        </v-layout>
        <v-layout v-else>
            Everything is registered !
        </v-layout>
    </section>
</template>


<script>
import Vue from 'vue';
import VeeValidate from 'vee-validate';

Vue.use(VeeValidate)

export default {
    data() {
        return {
            password: '',
            passwordConfirm: '',
            success: false
        }
    },
    methods: {
        submit() {
            var vm = this;
            this.$validator.validateAll().then(function(success) {
                if (!success) return;
                var credentials = {
                    password: vm.password,
                    auth_token: vm.$route.params.token //useless on serverside, useful for index.js
                }
                console.log("GOOD TO GO", credentials);
                vm.$store.dispatch('confirm', credentials)
                .then((response) => {
                    vm.success = true;
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
            })
        }
    }
}

</script>
<style type="text/css">
.error--text {
    color: #ff5252 !important;
}
</style>