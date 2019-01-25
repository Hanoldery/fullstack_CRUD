<template>
    <v-layout dense align-start>
        <v-card v-if="not_found">
            <v-card-title class="display-2">
                Vous n'avez pas accès à cette page.
            </v-card-title>
            <v-card-text>
                Pour revenir à l'accueil
                <v-btn flat @click="$router.push({path: '/'})">cliquez ici</v-btn>
            </v-card-text>
        </v-card>
        <v-card v-else-if="no_params == true">
            <v-card-title class="display-1">
                Cliquez sur un élément à Administrer
            </v-card-title>
        </v-card>
        <v-card v-else width="100%">
            <v-list two-line class="scrollbox darky">
                <v-flex xs12>
                    <v-list-tile>
                        <no-ssr>
                            <v-flex class="px-1 flex-min-8" v-for="title in thisStruct" :key="title">
                                <v-list-tile-content class="subheading font-weight-medium">
                                    {{cutId(title) | startCase}}
                                </v-list-tile-content>
                            </v-flex>
                            <v-flex class="px-1 flex-min-8">
                                <v-list-tile-content class="subheading font-weight-medium" v-if="!$store.state.loading">
                                    Delete
                                </v-list-tile-content>
                            </v-flex>
                        </no-ssr>
                    </v-list-tile>
                </v-flex>
                <v-data-iterator
                    :items="objects"
                    content-tag="v-layout"
                    row wrap
                    itemKey="['obj']['id']"
                    loading="primary"
                    :pagination.sync="pagination">
                    <template slot="no-data">
                        <no-ssr>
                            <v-layout justify-center width="100%">
                                <v-flex xs6 v-if="reactiveErrors.type == 'page'">
                                    <div class="display-1">
                                        L'objet n'existe pas ⚠️
                                    </div>
                                </v-flex>
                                <v-flex xs2 v-else-if="$store.state.loading">
                                    <v-progress-circular  :indeterminate="true" color="primary"></v-progress-circular>
                                </v-flex>
                                <v-flex xs6 v-else>
                                    <div class="display-1">
                                        Pas encore de données, ajoutez-en une avec ✚
                                    </div>
                                </v-flex>
                            </v-layout>
                        </no-ssr>
                    </template>
                    <v-flex slot="item" slot-scope="props" xs12>
                        <v-list-tile>
                            <FieldComponent v-for="(value, title, index) in itemFieldsFiltered(props.item['obj'])"
                                    :index.sync="index" :value.sync="value" :title.sync="title" :key="title + props.item['obj'].id"
                                    :object.sync="props.item" :related.sync="props.item['rel']" @click="display(title, index, value)"/>
                            <v-flex class="px-1 flex-min-8">
                                <v-list-tile-content>
                                    <v-btn @click="deleteItem(props.item['obj'].id)" flat icon color="red">
                                        <v-icon>mdi-trash-can-outline</v-icon>
                                    </v-btn>
                                </v-list-tile-content>
                            </v-flex>
                        </v-list-tile>
                    </v-flex>
                </v-data-iterator>
                <v-fab-transition v-show="this.$store.state.user.admin">
                    <v-btn
                        dark
                        fab
                        fixed
                        bottom
                        right>
                        <v-icon 
                        @click="createNew">mdi-plus</v-icon>
                    </v-btn>
                </v-fab-transition>
            </v-list>
        </v-card>
    </v-layout>
</template>



<script>
import Vue from 'vue';
import FieldComponent from '@/components/FieldComponent.vue';
import VeeValidate from 'vee-validate';
import { ErrorBag } from 'vee-validate';
import NoSSR from 'vue-no-ssr';
import _ from 'lodash';

const bag = new ErrorBag();

Vue.use(VeeValidate)

export default {
    data() {
        return {
            objects: [],
            not_found: false,
            no_params: Boolean,
            pagination: {
                page: 1,
                rowsPerPage: 5
            },
        }
    },
    provide: {
        $validator: '$validator'
    },
    components: {
        FieldComponent,
        'no-ssr': NoSSR,
    },
    computed: {
        reactiveObjects: function() {
            return this.$store.getters.objectsReactive;
        },
        reactiveErrors: function() {
            return this.$store.getters.errorReactive;
        },
        reactiveUser: function() {
            return this.$store.getters.userReactive;
        },
        thisStruct: function() {
            const vm = this;
            var storeStruct = [];
            var struct = {};
            for (var obj in this.$store.state.dbStruct) {
                if (obj == this.$route.params.object) {
                    storeStruct = this.$store.state.dbStruct[obj];
                    for (var field in storeStruct) {
                        struct[field] = storeStruct[field];
                    }
                }
            }
            return Object.keys(struct).filter(title => vm.isNotId(title));
        },
    },
    watch: {
        reactiveObjects: function() { // TODO: Refactor, too shity
            var vm = this;
            Vue.nextTick(function () {
                // Check for errors before sending to the back
                if (vm.objects.length == 0 || vm.objects.length != vm.$store.getters.objectsReactive.length) {
                    // TODO : arrange this 
                    // Maybe deleting next-tick will create problems
                    // it was a problem when creating a new object,
                    // so I duplicated.
                    vm.object = [];
                    Vue.nextTick(function () {
                        vm.objects = vm.$store.getters.objectsReactive;
                    });
                }
                var objects = vm.$store.getters.objectsReactive;
                var errors = vm.$store.getters.errorReactive;
                var object = [];
                // Si l'objet est juste on vide, on l'ajoute tout de même
                // à l'object courant pour qu'il s'affiche
                // if (errors && errors['message'].includes("is empty"))
                //     vm.obj
                if (errors && errors['type'] == 'field')
                    return vm.objects;
                for (var obj in objects) {
                    console.log("REACTIVE 1", vm.idInToUpdateObjects(objects[obj]['obj']['id']));
                    if (objects[obj]['obj'] && vm.idInToUpdateObjects(objects[obj]['obj']['id'])) {
                        object['route'] = vm.$route.params.object;
                        object['id'] = objects[obj]['obj']['id'];
                        object['obj'] = objects[obj]['obj'];
                        console.log("REACTIVE 2 ", object);
                        vm.$store.dispatch('sendObjectBack', object)
                            .then(response => {
                                vm.$store.commit('_showTooltip', {type: 'success', msg: "L'objet a été mis à jour 🤟"});
                            })
                            .catch(error => {
                                vm.force_refresh();
                                vm.$store.commit('_showTooltip', {type: 'fail', msg: "Erreur sur la base de donnée, vérifiez les champs, sinon contactez l'admin."});
                            });
                    }
                }
            });
        },
        '$route.params.object': function() {
            this.getDatas();
        }
    },
    methods: {
        itemFieldsFiltered: function(item) {
            var vm = this;
            var fields = Object.keys(item).filter((title, index, value) => vm.isNotId(title))
            var newItem = {};
            for (var field in fields)
                newItem[fields[field]] = item[fields[field]];
            return newItem;
        },
        idInToUpdateObjects: function(id) {
            for (var id_up in this.$store.state.objects_to_update) {
                if (this.$store.state.objects_to_update[id_up] == id)
                    return true;
            }
            return false;
        },
        errors: function() {
            var array = "";
            var vm = this;
            Vue.nextTick(function () {
                    var err = vm.$validator.errors.items;
                    for (var i in err) {
                        array += str(err[i]);
                    }
            });
            return array;
        },
        deleteItem: function(id) {
            var vm = this;
            var obj = {};
            obj["id"] = id;
            obj["route"] = vm.$route.params.object;
            vm.$store.dispatch('deleteObjectBack', obj)
                .then(() => {
                    vm.force_refresh();
                    vm.$store.commit('_showTooltip', {type: 'success', msg: "Objet détruit ! 🗑"});
                })
                .catch(error => {
                    vm.force_refresh();
                    vm.$store.commit('_showTooltip', {type: 'fail', msg: "Erreur, vérifiez les champs."});
                })
        },
        createNew: function() {
            var obj = [];
            obj['obj'] = {};
            obj['rel'] = {};
            for (var struct in this.$store.state.dbStruct) {
                if (struct == this.$route.params.object) {
                    for (var field in this.$store.state.dbStruct[struct]) {
                        if (field == "id")
                            obj['obj'][field] = this.$store.getters.objMaxId + 1;
                        else
                            obj['obj'][field] = null;
                        if (field.includes("_id")) {
                            if (field.includes(this.$route.params.object))
                                obj['rel'][field + '__nton'] = null;
                            else
                                obj['rel'][field] = null;
                        }
                    }
                }
            }
            var payload = {};
            for (var field in obj['rel']) {
                obj['rel'][field] = null;
            }
            payload["obj"] = obj['obj'];
            this.$store.commit("_addObject", obj);
            var error = {};
            error['type'] = 'field';
            error['message'] = 'New object is empty';
            this.$store.commit('_updateError', error);
        },
        isCompatible: function(key, type, include='') {
            var i = 0;
            if (!this.objectStruct) {
                return false;
            }
            while (i < this.$store.state.objectStruct.length) { // TODO: not good, too long, too shity
                if (this.$store.state.objectStruct[i] == key) {
                    if (this.$store.state.objectStruct[i].includes(type)) {
                        if (include.length > 0) {
                            if (this.$store.state.objectStruct[i].includes(include))
                                return true;
                            else
                                return false;
                        }
                        else {
                            return true; 
                        }
                    }
                    else {
                        return false;
                    }
                }
                i++;
            }
            return false;
        },
        isNotId: function(title) {
            if (title == 'id')
                return false;
            return true;
        },
        cutId: function(title) {
            return _.split(title, '_id', 1)[0];
        },
        force_refresh: function() {
            var vm = this;
            vm.objects = [];
            Vue.nextTick(function () {
                vm.objects = vm.$store.getters.objectsReactive;
                vm.pagination = {
                    page: 1,
                    rowsPerPage: 5
                }
            });
        },
        getDatas: function() {
            this.$store.commit('_updateLoading', true);
            this.$store.dispatch('getObjects', this.$route.params.object)
                .then(r => {
                    this.$store.commit('_updateLoading', false)
                    this.force_refresh();
                })
                .catch(err => {
                    console.log(err);
                    this.$store.commit('_updateLoading', false)
                })
        }
    },
    beforeCreate: function() {
        if (this.$store.state.error.type == 'page')
            return;
        this.$store.commit('_updateLoading', true);
        this.$store.dispatch('getObjects', this.$route.params.object)
            .then(r => {
                this.$store.commit('_updateLoading', false)
                this.force_refresh();
            })
            .catch(err => {
                console.log(err);
                this.$store.commit('_updateLoading', false)
            })
    },
    created: function() {
        this.$root.$on('refresh', this.force_refresh);
        var vm = this;
        Vue.nextTick(function () {
            if (!vm.$route.params.object)
                vm.no_params = true;
            else
                vm.getDatas();
        })
        // TODO: Re-activate those 'go fuck yourself' lines if you're not admin
        //          as it was for testing purpose only.
        // if (!this.reactiveUser.loading && !this.reactiveUser.admin)
        //     this.not_found = true;
    },
    destroyed: function() {
        this.$root.$off('refresh');
    }
}

</script>