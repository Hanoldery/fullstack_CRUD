<template>
   	<v-list-tile-content>
        <v-switch
            v-model="value"
            color="purple darken-3"
            v-on:change="fieldChanged">
        </v-switch>
        <span class="caption" v-html='boolDisplay'>{{ boolDisplay }}</span>
    </v-list-tile-content>
</template>

<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
const Vuetify = require("vuetify").default

export default {
	data() {
		return {
			value: Boolean,
		}
	},
    name: 'booleanField',
    inject: ['$validator'],
    mixins: [mixinAdminField],
    props: ['field'],
    computed: {
        boolDisplay: function() {
            return (this.field.value === true)? this.field.title : 'No ' + this.field.title;
        },
    },
    mounted: function() {
        this.$validator.validateAll();
        if (this.$props.field.value == null) {
            this.value = true;
            this.fieldChanged(true);
        }
        else {
            this.value = this.$props.field.value;
        }
    }
}
</script>