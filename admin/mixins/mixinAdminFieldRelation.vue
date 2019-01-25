<script>
import Vue from 'vue';

export default  {
    data() {
        return {
            relatedObj: [],
            relatedObjSelect: null,
            relatedObjNtoN: [],
            relatedObjNtoNCopy: [],
            relatedObjNtoNSub: [],
            NtonLoadError: '',
            title: '',
        }
    },
    name: 'mixinAdminFieldRelation',
    computed: {
        relatedNton: function() {
            if (this.field.title.indexOf(this.$route.params.object + "_") == 0)
                return this.field.title.substring(
                    this.field.title.indexOf(this.$route.params.object + "_")
                    + this.$route.params.object.length + 1, this.field.title.length
                );
            else
                return this.field.title.substring(0, this.field.title.indexOf("_" + this.$route.params.object));
        },
    },
    methods: {
        relatedObjNtoNFiltered() {
            const vm = this;
            if (_.isEmpty(this.relatedObjNtoN))
                return [];
            return this.relatedObjNtoN.filter(m => vm.applySearch(m.title));
        },
        cutId: function(title) {
            return _.split(title, '_id', 1)[0];
        },
        ntonDiffers: function(id) {
            return (this.relatedObjNtoNCopy[id]["selected"] != this.relatedObjNtoN[id]["selected"]
                    || this.relatedObjNtoNCopy[id]["sub"] != this.relatedObjNtoN[id]["sub"]);
        },
        updateNton: function() {
            var other = _.cloneDeep(this.relatedNton);
            var subTitle = this.relatedObjNtoN[0]["subTitle"] + "_id"; // CHECK this one good

            for (var id in this.relatedObjNtoNCopy) {
                if (this.ntonDiffers(id)) {
                    var rel = {};
                    rel['obj'] = {};
                    rel["route"] = this.title + "_nton";
                    rel['obj'][other + "_id"] = this.relatedObjNtoNCopy[id]["id"];
                    rel['obj'][subTitle] = this.relatedObjNtoN[id]["sub"];
                    rel['obj'][this.$route.params.object + "_id"] = this.field.object['obj']["id"];

                    if (this.relatedObjNtoNCopy[id]["selected"] &&
                        !this.relatedObjNtoN[id]["selected"])
                        this.updateNtonUnselect(rel);
                    else
                        this.updateNtonSelect(rel);
                }
            }
        },
        updateNtonSelect: function(bundleRelToAdd) {
            var vm = this;
            vm.$store.dispatch('sendObjectBack', bundleRelToAdd)
                .then(response => {
                    vm.$store.commit('_showTooltip', {type: 'success', msg: "Selected Relation"});
                    vm.relatedObjNtoNCopy = _.cloneDeep(vm.relatedObjNtoN);
                })
                .catch(error => {
                    console.log(error);
                    vm.$store.commit('_showTooltip', {type: 'fail', msg: "Selecting Relation Failed"});
                })
        },
        updateNtonUnselect: function(relToDel) {
            var vm = this;
            vm.$store.dispatch('deleteObjectBack', relToDel)
                .then(response => {
                    vm.$store.commit('_showTooltip', {type: 'success', msg: "Unselected Relation"});
                    vm.relatedObjNtoNCopy = _.cloneDeep(vm.relatedObjNtoN);
                })
                .catch(error => {
                    console.log("ERR ", error);
                    vm.$store.commit('_showTooltip', {type: 'fail', msg: "Unselecting Relation Failed"});
                });
        },
        loadRelated: function() {
            console.log("LOADREALTED ", this.relatedObj, this.cutId(this.title), this.title);
            // TODO: faire remonter cette fonction et partager ses résultat entre les components
            if (this.relatedObj.length > 1)
                return;
            this.$axios.$get('/get/' + this.cutId(this.title))
            .then((response) => {
                var rslt = [];
                console.log("LOADREALTED 1", response);
                for (var i in response)
                    rslt = _.concat(rslt, response[i]['obj']);
                this.relatedObj = rslt;
            })
            .catch((error) => {
                console.log(error);
                console.log(error.response); 
            })
        },
        extractNtoNSub: function(other) {
            for (var fieldName in this.$store.state.dbStruct[this.title]) {
                if (_.split(fieldName, '_id', 1)[0] != this.$route.params.object &&
                    _.split(fieldName, '_id', 1)[0] != other)
                    return _.split(fieldName, '_id', 1)[0];
            }
        },
        getNtonOther: async function(other, sub) {
            try {
                var responseRel = await this.$axios.$get('/get/' + other);
                for (var i in responseRel) {
                    var current = responseRel[i]['obj'];
                    current["selected"] = false;
                    current["sub"] = 1;
                    current["subTitle"] = sub;
                    this.relatedObjNtoN = _.concat(this.relatedObjNtoN, current);
                }
            }
            catch (e) {
                this.NtonLoadError = 'Nodata';
                this.relatedObjNtoN = [];
                return 1;
                console.log(e);
            }
        },
        getNtonSub: async function(sub) {
            try {
                var responseRel = await this.$axios.$get('/get/' + sub);
                for (var i in responseRel)
                    this.relatedObjNtoNSub = _.concat(this.relatedObjNtoNSub, responseRel[i]['obj']);
            }
            catch (e) {
                this.NtonLoadError = 'Nodata';
                this.relatedObjNtoN = [];
                console.log(e);
                return false;
            }
        },
        loadNtoNRelated: async function() {
            this.displayDialog = true;
            // TODO: faire remonter cette fonction et partager ses résultat entre les components
            // For related if str - "nton" == title, get each field except if == title
            // Launch request with each field, get object, selected is related if str - "nton" == title

            var other = _.cloneDeep(this.relatedNton);
            var field_format;
            var sub = this.extractNtoNSub(other);
            console.log("FIRST LOAD ", newRelatedObjNton);
            if (this.relatedObjNtoN.length == 0) {
                console.log("NUUUULLL");
                if (await this.getNtonOther(other, sub) == 1)
                    return 1;
            }
            if (this.relatedObjNtoNSub.length == 0 && sub)
                if (await this.getNtonSub(sub) == false)
                    return 1;
            var newRelatedObjNton = _.cloneDeep(this.relatedObjNtoN);

            try {
                console.log("TEST LOAD NTON ", this.title + "_nton", newRelatedObjNton[0])
                var response = await this.$axios.$get('/get/' + this.title + "_nton");
                for (var i in response) {
                    var current = response[i]['obj'];
                    if (current[this.$route.params.object + "_id"] == this.field.object['obj']["id"]) {
                        for (var objRel in newRelatedObjNton) {
                            if (newRelatedObjNton[objRel]["id"] == current[other + '_id']) {
                                newRelatedObjNton[objRel]["selected"] = true;
                                newRelatedObjNton[objRel]["sub"] = current[sub + "_id"];
                            }
                        }
                    }
                }
            }
            catch (e) {
                console.log(e);
            }
            this.relatedObjNtoNCopy = _.cloneDeep(newRelatedObjNton);
            console.log("FINISHED LOAD ", this.relatedObjNtoNCopy, newRelatedObjNton);
            this.$set(this, 'relatedObjNtoN', newRelatedObjNton)
        }
    }
}
</script>