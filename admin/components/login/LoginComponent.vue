<template>
    <!-- TODO: Update this, Login is now a 
        component dialog should never be changed as it's a pro, fix that -->
    <v-dialog
        v-model="dialog"
        hide-overlay
        transition="dialog-bottom-transition"
        max-width="50%"
        scrollable>
        <v-card class="pa-3">
            <v-card-title>
                <span v-if="type == 'login'" class="headline">Login</span>
                <span v-else-if="type == 'register'" class="headline">Register</span>
            </v-card-title>
            <v-card-text>
                <v-layout v-if="type == 'great'">
                    <h4>You'll receive an email to set your password and access your account !</h4>
                </v-layout>
                <v-layout v-if="type == 'login'">
                    <form>
                        <v-text-field
                            label="Email"
                            data-vv-name="email"
                            v-validate="'required|email'"
                            v-model="credentials.email"
                            ref="email"
                            :error-messages="errors.collect('email')"
                            required>
                        </v-text-field>
                        <v-text-field
                            label="Password"
                            data-vv-name="password"
                            v-validate="'required'"
                            v-model="credentials.password"
                            ref="password"
                            :error-messages="errors.collect('password')"
                            type="password"
                            required>
                        </v-text-field>
                        You don't have an account ?
                        <v-btn color="darken-1" flat @click.native="type = 'register'">Register</v-btn><br/>
                        You forgot your password ?
                        <v-btn color="darken-1" flat @click.native="type = 'reset'">Reset Password</v-btn>
                    </form>
                </v-layout>
                <v-layout v-else-if="type == 'register'">
                    <form>
                        <v-text-field
                            v-validate="'required|email'"
                            v-model="credentials.email"
                            :error-messages="errors.collect('email')"
                            label="E-mail"
                            data-vv-name="email"
                            required>
                        </v-text-field>
                        <v-text-field
                            v-validate="'required|max:20'"
                            v-model="credentials.title"
                            :counter="30"
                            :error-messages="errors.collect('title')"
                            label="Name"
                            data-vv-name="title"
                            required>
                        </v-text-field>
                        Already registered ?
                        <v-btn color="darken-1" flat @click.native="type = 'login'">Login</v-btn>
                    </form>
                </v-layout>
                <v-layout v-else-if="type == 'reset'">
                    <form>
                        <v-text-field
                            v-validate="'required|email'"
                            v-model="credentials.email"
                            :error-messages="errors.collect('email')"
                            label="E-mail"
                            data-vv-name="email"
                            required>
                        </v-text-field>
                        <v-btn color="darken-1" flat @click.native="type = 'login'">← Go Back</v-btn><br/>
                    </form>
                </v-layout>
                <v-layout>
                    {{errorMessage}}
                </v-layout>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-if="type == 'login'" @click.native="login">Login</v-btn>
                <v-btn v-else-if="type == 'register'" color="darken-1" @click.native="register">Register</v-btn>
                <v-btn v-else-if="type == 'reset'" color="darken-1" @click.native="passwordReset">Send Reset Link</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    name: 'LoginComponent',
    props: ['dialog'],
    data() {
        return {
            // TOOD: Change the following as data is not going up
            type: "login",
            credentials: {
                email: '',
                password: '',
                title: '',
            },
            errorMessage: ''
        }
    },
    methods: {
        logout() {
            this.$store.dispatch('logout');
        },
        login() {
            var vm = this;
            this.$validator.validateAll().then(function(success) {
                if (!success) return;
                var credentials = {
                    email: vm.credentials.email,
                    password: vm.credentials.password
                }
                vm.$store.dispatch('login', credentials)
                .then(response => {
                    this.$emit('closeDialog')
                })
                .catch(error => {
                    if (error.response) {
                        vm.errorMessage = error.response.data.error;

                        const field = vm.$validator.fields.find({title: 'email', scope: vm.$options.scope });

                        if (!field) return;

                        vm.$validator.errors.add({
                            id: field.id,
                            field: 'email',
                            msg: error.response.data.message,
                            scope: vm.$options.scope,
                        });

                        field.setFlags({
                            invalid: true,
                            valid: false,
                            validated: true,
                        });
                    }
                })
            })
        },
        passwordReset() {
            var vm = this;
            this.$validator.validateAll().then(function(success) {
                if (!success) return;
                var credentials = {
                    email: vm.credentials.email
                }
                vm.$store.dispatch('passwordReset', credentials)
                .then((response) => {
                    vm.type = "great";
                    setTimeout(function () {
                        this.$emit('closeDialog')
                        setTimeout(function () {
                            vm.type = "login";
                        }, 500);
                    }, 10000);
                })
                .catch((error) => {
                    vm.errorMessage = error.response.data.error;

                    const field = this.$validator.fields.find({ title: 'email', scope: vm.$options.scope });

                    if (!field) return;

                    vm.$validator.errors.add({
                        id: field.id,
                        field: 'email',
                        msg: error.response.data.message,
                        scope: vm.$options.scope,
                    });

                    field.setFlags({
                        invalid: true,
                        valid: false,
                        validated: true,
                    });
                });
            }) 
        },
        register() {
            var vm = this;
            this.$validator.validateAll().then(function(success) {
                if (!success) return;
                var credentials = {
                    email: vm.credentials.email,
                    title: vm.credentials.title
                }
                console.log("CREDS", credentials);
                vm.$store.dispatch('register', credentials)
                .then((response) => {
                    vm.type = "great";
                    setTimeout(function () {
                        this.$emit('closeDialog')
                        setTimeout(function () {
                            vm.type = "login";
                        }, 500);
                    }, 10000);
                })
                .catch((error) => {
                    vm.errorMessage = error.response.data.error;

                    const field = vm.$validator.fields.find({ title: 'email', scope: vm.$options.scope });

                    if (!field) return;

                    vm.$validator.errors.add({
                        id: field.id,
                        field: 'email',
                        msg: error.response.data.message,
                        scope: vm.$options.scope,
                    });

                    field.setFlags({
                        invalid: true,
                        valid: false,
                        validated: true,
                    });
                });
            })
        }
    }
}
</script>