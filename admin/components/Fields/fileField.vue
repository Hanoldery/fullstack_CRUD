<template>
    <v-list-tile-avatar v-if="fileType == 'image'">
        <fileFieldInput :field="field" :fileType="fileType" />
    </v-list-tile-avatar>

    <v-list-tile-content v-else>
        <fileFieldInput :field="field" :fileType="fileType" />
    </v-list-tile-content>
</template>

<script> 
import Vue from 'vue';
import fileFieldInput from '@/components/Fields/fileFieldInput.vue';
const Vuetify = require("vuetify").default

export default {
    inject: ['$validator'],
    name: 'fileField',
    components: {
        fileFieldInput
    },
    props: ['field', 'fileType']
}
</script>