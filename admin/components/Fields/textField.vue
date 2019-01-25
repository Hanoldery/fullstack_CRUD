<template>
    <v-list-tile-content>
        <v-text-field
            :ref="field.title + field.object['obj'].id"
            v-validate="isNullable(field.title) ? '' : 'required'"
            v-model="field.value"
            color="primary"
            :error-messages="errors.collect(field.title + field.object['obj'].id)"
            :error="errors.has(field.title + field.object['obj'].id)"
            :data-vv-name="field.title + field.object['obj'].id"
            :required="isNullable(field.title) ? false : true"
            @input="fieldChanged"/>
    </v-list-tile-content>
</template>

<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
const Vuetify = require("vuetify").default

export default {
    name: 'textField',
    inject: ['$validator'],
    mixins: [mixinAdminField],
    props: ['field']
}
</script>