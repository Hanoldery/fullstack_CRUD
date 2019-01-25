import Vuex from 'vuex';
import Vue from 'vue';

const saveStore = store => {
    store.subscribe((mutation, state) => {
        if (process.browser && state) {
            var cache = [];
            localStorage.setItem('store', JSON.stringify(state,
                function(key, value) {
                    if (typeof value === 'object' && value !== null) {
                        if (cache.indexOf(value) !== -1) {
                            try {
                                return JSON.parse(JSON.stringify(value));
                            } catch (error) {
                                return;
                            }
                        }
                        cache.push(value);
                    }
                    return value;
                })
            );
            cache = null;
        }
    })
}

const createStore = () => {
    return new Vuex.Store({
        plugins: [saveStore],
        state: {
            counter: 0,
            user: {
                id: '',
                title: '',
                email: '',
                admin: '',
                auth_token: '',
                loading: true,
            },
            loading: true,
            objects: [],
            objects_backup: [],
            objects_to_update: [],
            dbStruct: {},
            error: {
                type: '',
                message: '',
            },
            tooltip: {
                success: {
                    state : false,
                    msg: '',
                },
                fail: {
                    state : false,
                    msg: '',
                },
                
            }
        },
        getters: {
            objectsReactive(state) {
                return state.objects;
            },
            objMaxId(state) {
                var i = 0;
                for (var obj in state.objects)
                    if (state.objects[obj]['obj']['id'] > i)
                        i = state.objects[obj]['obj']['id'];
                return i;
            },
            userReactive: state => state.user,
            errorReactive: state => state.error,
            dbStructReactive: state => state.dbStruct,
            tooltipSuccess: state => state.tooltip.success.state,
            tooltipSuccessMsg: state => state.tooltip.success.msg,
            tooltipFail: state => state.tooltip.fail.state,
            tooltipFailMsg: state => state.tooltip.fail.msg,
        },
        mutations: {
            initialiseStore(state, commit) {
                if (process.browser &&
                    localStorage.getItem('store') &&
                    localStorage.getItem('store') != 'undefined') {
                    var stateKeys = Object.keys(state).sort();
                    var localKeys = Object.keys(JSON.parse(localStorage.getItem('store')));
                    var error = 0;
                    for (var key in stateKeys) {
                        if (!localKeys.includes(stateKeys[key]))
                            error++;
                    }
                    if (error == 0) 
                        Vue.set(state, 'user', JSON.parse(localStorage.getItem('store'))['user']);
                    state.user.loading = false;
                }
            },
            _login(state, user) {
                state.user = user;
            },
            _logout(state) {
                var user_empty = {
                    id: '',
                    title: '',
                    email: '',
                    admin: '',
                    auth_token: '',
                };
                state.user = user_empty;
            },
            _updateObject(state, object) {
                console.log("_updateObject ", object);
                for (var obj_i in state.objects) {
                    console.log("_updateObject 1", state.objects[obj_i]['obj'], object);
                    if (state.objects[obj_i]['obj'].id == object['obj']['id']) {
                        Vue.set(state.objects, obj_i, object);
                    }
                }
            },
            _deleteObject(state, object) {
                var i = 0;
                for (var obj in state.objects) {
                    if (state.objects[obj]['obj']['id'] == object['obj']['id'])
                        state.objects.splice(i, 1);
                    i++;
                }
            },
            _addObject(state, object) {
                if (state.objects.length == 0) {
                    var dup = {};
                    dup["obj"] = _.cloneDeep(object["obj"]);
                    dup["rel"] = _.cloneDeep(object["obj"]);
                    state.objects.push(_.cloneDeep(dup));
                }
                else
                    state.objects = _.concat(state.objects, _.cloneDeep(state.objects[0]));
                for (var field in state.objects[0]['obj']) {
                    state.objects[0]['obj'][field] = object['obj'][field];
                }
                for (var field in state.objects[0]['rel']) {
                    state.objects[0]['rel'][field] = object['rel'][field];
                }
            },
            _updateLoading(state, bool) {
                Vue.set(state, 'loading', bool);
            },
            _updateObjects(state, objects) {
                state.objects = objects;
            },
            _updateObjectsSave(state, objects) {
                state.objects_backup = objects;
            },
            _updateObjectsStruct(state, objectStruct) {
                state.objectStruct = objectStruct;
            },
            _addObjectsToUpdate(state, id) {
                var i = 0;
                for (var obj in state.objects_to_update) {
                    if (state.objects_to_update[obj] == id) {
                        return;
                    }
                    i++;
                }
                state.objects_to_update = _.concat(_.cloneDeep(id), state.objects_to_update);
            },
            _delObjectsToUpdate(state, id) {
                var i = 0;
                for (var obj in state.objects_to_update) {
                    if (state.objects_to_update[obj] == id) {
                        state.objects_to_update.splice(i, 1);
                    }
                    i++;
                }
            },
            _updateError(state, error) {
                state.error = error;
            },
            _updateDbStruct(state, dbStruct) {
                state.dbStruct = dbStruct;
            },
            _showTooltip(state, tooltip) {
                state.tooltip[tooltip['type']]['state'] = true;
                state.tooltip[tooltip['type']]['msg'] = tooltip['msg'];
                setTimeout(function() {
                    state.tooltip[tooltip['type']]['state'] = false;
                }, 2000);
            },
        },
        actions: {
            async nuxtServerInit ({ commit, dispatch, state }) {
                await dispatch('getDbStruct', this.$route)
                    .then(response => {
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            logout({ commit }) {
                commit('_logout');
            },
            login({ dispatch, state, commit }, credentials) {
                return new Promise((resolve, reject) => {
                    this.$axios.$post('/login', credentials)
                        .then((response) => {
                            console.log(response);
                            commit('_login', response)
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log(error);
                            console.log(error.response);
                            reject(error);
                        })
                })
            },
            passwordReset({ dispatch, state, commit }, credentials) {
                return new Promise((resolve, reject) => {
                    this.$axios.$post('/password_reset', credentials)
                        .then((response) => {
                            console.log(response);
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log(error);
                            reject(error);
                        })
                })
            },
            register({}, credentials) {
                return new Promise((resolve, reject) => {
                    this.$axios.$post('/register', credentials)
                        .then((response) => {
                            console.log(response);
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log(error);
                            console.log(error.response);
                            reject(error);
                        })
                })
            },
            confirm({}, credentials) {
                return new Promise((resolve, reject) => {
                    this.$axios.$post('/confirm/' + credentials['auth_token'], credentials)
                        .then((response) => {
                            console.log(response);
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log(error);
                            console.log(error.response);
                            reject(error);
                        })
                })
            },
            async getDbStruct({ dispatch, state, commit }, route) {
                return new Promise((resolve, reject) => {
                    this.$axios.$get('/api/db_structure')
                        .then((response) => {
                            if (!response) {
                                var error = {};
                                console.log("INDEX failed no response", response);
                                error['type'] = 'database';
                                error['message'] = 'DB error';
                                commit('_updateError', error);
                                return reject(error);
                            }
                            commit('_updateDbStruct', response);
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log(error);
                            console.log(error.response);
                            reject(error);
                        })
                });
            },
            checkObjectExist({state, commit}, route) {
                return new Promise((resolve, reject) => {
                    if (!route.params.object || !route.path.includes("admin"))
                        return resolve(true);
                    for (var obj in state.dbStruct)
                        if (route.params.object == obj)
                            return resolve(true);
                    commit('_updateLoading', false);
                    commit('_updateError', {type: 'page', message: 'This page doesn\'t exist'});
                    return reject({type: 'page', message: 'This page doesn\'t exist'});
                });
            },
            getObjects({ dispatch, state, commit }, object) {
                return new Promise((resolve, reject) => {
                    var creds = {};
                    creds['email'] = state.user.email;
                    creds['auth_token'] = state.user.auth_token;
                    this.$axios.$post('/get/' + object, creds)
                        .then((response) => {
                            if (response) {
                                commit('_updateObjects', response);
                                commit('_updateObjectsSave', response);
                            }
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log("FAIL obj ");
                            var empty = [];
                            commit('_updateObjects', empty);
                            reject(error);
                            console.log(error);
                            console.log(error.response);
                        });
                })
            },
            getObjectsFiltered({ dispatch, state, commit }, object) {
                return new Promise((resolve, reject) => {
                    console.log("GET OBJECTS FILTERED ");
                    var json = {};
                    json['email'] = state.user.email;
                    json['auth_token'] = state.user.auth_token;
                    _.merge(json, object);
                    this.$axios.$post('/get/' + object['type'], json)
                        .then((response) => {
                            console.log("SUCCEED obj ");
                            commit('_updateObjects', response);
                            commit('_updateObjectsSave', response);
                            resolve(response);
                        })
                        .catch((error) => {
                            console.log("FAIL obj ");
                            reject(error);
                            console.log(error);
                            console.log(error.response);
                        });
                })
            },
            //TODO: Test this.
            deleteObjectBack({ state, commit }, bundle) {
                return new Promise((resolve, reject) => {
                    var obj = {};
                    if (bundle['id']) {
                        for (var _id in state.objects) {
                            if (state.objects[_id]['obj']["id"] == bundle['id']) {
                                obj = state.objects[_id];
                            }
                        }
                    }
                    else
                        obj['obj'] = bundle['obj'];
                    this.$axios.$post('/delete/' + bundle['route'], obj['obj'])
                    .then(response => {
                        if (bundle['id'])
                            commit("_deleteObject", obj);
                        resolve();
                    })
                    .catch(error => {
                        console.log(error);
                        reject();
                    })
                });
            },
            sendObjectBack({ state, commit }, bundle) {
                return new Promise((resolve, reject) => {
                    this.$axios.$post('/update/' + bundle['route'],  bundle['obj']) // CHECK if good one
                        .then((response) => {
                            if (bundle['id'])
                                commit('_delObjectsToUpdate', bundle['id']);
                            resolve(response);
                        })
                        .catch((error) => {
                            reject(error);
                        })
                });
            },
            getObjectState({ dispatch, state, commit }, id) {
                return new Promise((resolve, reject) => {
                    for (var obj_i in state.objects) {
                        if (state.objects[obj_i]['obj'].id ==  id) {
                            commit('_addObjectsToUpdate', id);
                            return resolve(state.objects[obj_i]);
                        }
                    }
                    reject();
                });
            },
            fillObjectState({ dispatch, state, commit }, object) {
                return new Promise((resolve, reject) => {
                    dispatch("getObjectState", object['id'])
                        .then(response => {
                            var object_state = response;
                            if (!object_state)
                                resolve(object['obj']);
                            if (object['rel']) {
                                for (var field_state in object_state['rel']) {
                                    if (object['rel'] == field_state + "_id") {
                                        object_state['rel'][field_state] = [object['obj']]; // object['rel'] ?
                                    }
                                }
                                object_state['obj'][object['rel']] = object['obj']['id'];
                            }
                            else {
                                for (var field_state in object_state['obj']) {
                                    for (var field in object['obj']) {
                                        if (field == field_state && field != "id") {
                                            object_state['obj'][field_state] = object['obj'][field];
                                        }
                                    }
                                }
                            }
                            resolve(object_state);
                        })
                        .catch(error => {
                            reject();
                        })
                });
            },
            updateObject({ dispatch, state, commit }, bundle) {
                return new Promise((resolve, reject) => {
                    // TODO: Check if file is working
                    // var file = '';
                    // if (bundle['obj'] && bundle['obj']['file']) {
                    //     file = bundle['obj']['file'];
                    //     delete bundle['obj']['file'];
                    // }

                    dispatch("fillObjectState", bundle)
                    .then(response => {
                        bundle['obj'] = response;
                        console.log("updateObject ", bundle);
                        commit("_updateObject", bundle['obj']);
                        resolve();
                    })
                    .catch(error => {
                        reject();
                    });
                });
            }
        }
    })
}

export default createStore
