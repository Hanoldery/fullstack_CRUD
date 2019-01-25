<template>
    <v-flex class="px-1 flex-min-8">
        <fileField :field="field" fileType="image" v-if="isCompatible(field.title, 'VARCHAR', 'image')"/>

        <fileField :field="field" fileType="audio" v-else-if="isCompatible(field.title, 'VARCHAR', 'media_url')"/>

        <fileField :field="field" fileType="video" v-else-if="isCompatible(field.title, 'VARCHAR', 'video_url')"/>

        <textField :field="field" v-else-if="isCompatible(field.title, 'VARCHAR')"/>

        <booleanField :field="field" v-else-if="isCompatible(field.title, 'BOOLEAN')"/>

        <relatedField :field="field" v-else-if="isCompatible(field.title, 'INTEGER', '_id')"/>

        <numberField :field="field" v-else-if="isCompatible(field.title, 'INTEGER')"/>

        <dateField :field="field" v-else-if="isCompatible(field.title, 'DATE')"/>

        <ntonField :field="field" v-else-if="isCompatible(field.title, 'NTON')"/>
    </v-flex>
</template>


<script> 
import Vue from 'vue';
import fileField from '@/components/Fields/fileField.vue';
import textField from '@/components/Fields/textField.vue';
import numberField from '@/components/Fields/numberField.vue';
import dateField from '@/components/Fields/dateField.vue';
import relatedField from '@/components/Fields/relatedField.vue';
import ntonField from '@/components/Fields/ntonField.vue';
import booleanField from '@/components/Fields/booleanField.vue';
const Vuetify = require("vuetify").default

export default {
    inject: ['$validator'],
    name: 'FieldComponent',
    props: ['index', 'title', 'value', 'type', 'object', 'related'],
    components: {
        fileField,
        textField,
        relatedField,
        numberField,
        dateField,
        ntonField,
        booleanField
    },
    data() {
        return {
            timeout: null,
            relatedObj: [],
            relatedObjSelect: null,
            relatedObjNtoN: [],
            relatedObjNtoNCopy: [],
            relatedObjNtoNSub: [],
            NtonLoadError: '',
            searchElement: "",
            imageData: '',
            field: {
                index: _.clone(this.$props.index),
                title: _.clone(this.$props.title),
                value: _.clone(this.$props.value),
                type: _.clone(this.$props.type),
                object: _.clone(this.$props.object),
                related: _.clone(this.$props.related),
            },
            displayDialog: false,
        }
    },
    watch: {
        value: function(newVal, oldVal) {
            this.field.index = _.clone(this.$props.index);
            this.field.title = _.clone(this.$props.title);
            this.field.value = _.clone(this.$props.value);
            this.field.type = _.clone(this.$props.type);
            this.field.object = _.clone(this.$props.object);
            this.field.related = _.clone(this.$props.related);
        },
    },
    methods: {
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
        cutId: function(title) {
            return _.split(title, '_id', 1)[0];
        },
    },
    mounted: function() {
        this.$validator.validateAll();
        if (!this.$props.object['rel'][this.cutId(this.$props.title)])
            return;
        this.relatedObj = [{
                'id': this.$props.value,
                'title': this.$props.object['rel'][this.cutId(this.$props.title)][0]['title']
            }];
        this.relatedObjSelect = _.cloneDeep(this.relatedObj[0]['id']);
        if (!this.relatedObjSelect)
            return;
        this.$validator.validateAll();
    },
};
</script>
<style>
.application>.v-overlay {
    z-index: 10 !important;
}
</style>