<template>
    <v-list-tile-content>
        <v-menu
            ref="menu"
            :close-on-content-click="false"
            v-model="displayMenu"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            min-width="290px"
          >
            <v-text-field
                slot="activator"
                v-model="computedDateFormated"
                label="Pick a date"
                v-validate="isNullable(field.title) ? '' : 'required'"
                :data-vv-name="field.title + field.object['obj'].id"
                :error-messages="errors.collect(field.title + field.object['obj'].id)"
                :error="errors.has(field.title + field.object['obj'].id)"
                readonly
            ></v-text-field>
            <v-date-picker
                v-model="field.value"
                v-validate="isNullable(field.title) ? '' : 'required'"
                :data-vv-name="field.title + field.object['obj'].id"
                no-title
                scrollable
                @input="fieldChanged"
                >
            </v-date-picker>
        </v-menu>
    </v-list-tile-content>
</template>
<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
const Vuetify = require("vuetify").default

export default {
    name: 'dateField',
    inject: ['$validator'],
    mixins: [mixinAdminField],
    props: ['field'],
    computed:{
        computedDateFormated: function() {
            return this.formatDate(this.field.value)
        },
    },
    methods: {
        formatDate (date) {
            if (!date) return null

            const [year, month, day] = date.split('-')
            return `${day}/${month}/${year}`
        },
    }
}
</script>