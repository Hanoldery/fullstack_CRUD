<script>
import Vue from 'vue';

export default  {
    data() {
        return {
            timeout: null,
            displayMenu: false,
        }
    },
    name: 'mixinAdminField',
    methods: {
        filterObjectRejectString(object, stringToReject) {
            return Object.keys(object)
                .filter(key => !_.includes(key, stringToReject))
                .reduce(
                    (obj, key) => {
                        obj[key] = object[key];
                        return obj;
                    }, {}
                );
        },
        findObjInStruct: function() {
            var storeStruct = [];
            var struct = {};
            for (var object in this.$store.state.dbStruct) { // TODO: CHECK this
                if (object == this.$route.params.object) {
                    storeStruct = this.$store.state.dbStruct[object];
                    for (var field in storeStruct) {
                        struct[field] = storeStruct[field];
                    }
                }
            }
            return struct;
        },
        isNullable: function(key){
            var struct = this.findObjInStruct();
            if (struct[key]['nullable'] == "False")
                return false;
            return true;
        },
        isCompatible: function(key, type, include='') {
            var rslt = false;
            var struct = this.findObjInStruct();
            if (struct != null && struct[key] && !(struct[key] == 'id'
                && struct[key]['type'] != undefined)) {
                if (struct[key]['type'].includes(type)
                    && (include.length == 0 || (include.length > 0
                    && key.includes(include)))) { // TODO: Clean what this if is doing
                    rslt = true;
                    if (struct[key]['type'].includes("DATE")
                        && this.field.value) {
                        this.field.value = this.field.value.split('T')[0]
                    }
                    else if (struct[key]['type'].includes("BOOLEAN")) {
                        if (this.field.value == 'true')
                            this.field.value = true;
                        else
                            this.field.value == false;
                    }
                }
                else
                    rslt = false;
            }
            else
                rslt = false;
            return rslt;
        },
        fieldChanged: function(data) {
            var vm = this;
            var error = _.cloneDeep(this.$store.state.error);
            error["type"] = null;
            error["message"] = null;
            var errorBag = null;
            vm.displayMenu = false;
            clearTimeout(vm.timeout);
            vm.timeout = setTimeout(function () {
                vm.$store.commit('_updateError', error);
                Vue.nextTick(function () {
                    console.log("FIELD CHANGED 0");
                    vm.$validator.validateAll()
                    .then(() => {
                        console.log("FIELD CHANGED 1");
                        errorBag = vm.$validator.errors.items;
                        for (var i in errorBag) {
                            error['type'] = 'field';
                            error['message'] = errorBag[i]['field'];
                            vm.$store.commit('_updateError', error);
                        }
                        if (vm.isCompatible(vm.field.title, 'NTON')) {
                            vm.updateNton(vm);
                        }
                        else {
                            vm.updateField(vm, data);
                        }
                    });
                });
            }, 1000);
        },
        updateField: function(vm, data) {
            // We don't send it directly to the back as some information may still
            // be missing. We udpate the store and the parent component, check
            // if everything is ok and then send it to the back.
            var bundle = {};
            bundle["id"] = vm.field.object['obj'].id;
            bundle["route"] = vm.$route.params.object;
            bundle["obj"] = {};
            if (vm.isCompatible(vm.field.title, 'INTEGER', '_id')) {
                for (var subObj in vm.relatedObj) {
                    if (vm.relatedObj[subObj]['id'] == vm.relatedObjSelect) {
                        bundle["obj"] = vm.relatedObj[subObj];
                    }
                }
                bundle["rel"] = vm.field.title;
            }
            else {
                bundle["obj"][vm.field.title] = data;
                bundle["obj"]["id"] = vm.field.object['obj'].id;
            }
            vm.$store.dispatch('updateObject', bundle)
                .then(response => {
                    vm.$store.commit('_showTooltip', {type: 'success', msg: "Updated Field !"});
                })
                .catch(error => {
                    console.log(error);
                    vm.$store.commit('_showTooltip', {type: 'fail', msg: "Erreur, contactez l'admin."});
                })
        },
    }
}
</script>