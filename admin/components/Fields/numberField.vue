<template> 
    <v-list-tile-content>
        <v-text-field
            :label="field.title"
            v-model="field.value"
            v-validate="isNullable(field.title) ? '' : 'required'"
            :error-messages="errors.collect(field.title + field.object['obj'].id)"
            :error="errors.has(field.title + field.object['obj'].id)"
            :data-vv-name="field.title + field.object['obj'].id"
            mask="#####"
            solo
            @input="fieldChanged">
        </v-text-field>
    </v-list-tile-content>
</template>

<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
const Vuetify = require("vuetify").default

export default {
    name: 'numberField',
    inject: ['$validator'],
    mixins: [mixinAdminField],
    props: ['field']
}
</script>