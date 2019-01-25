<template>
    <v-list-tile-content>
        <!-- {{formatRelation(this.$props.object[1][cutId(title)]['obj'])}} -->
        <!-- {{ relatedObj[cutId(title)] }} -->

        <v-select
            v-model="relatedObjSelect"
            :items="relatedObj"
            item-text="title"
            item-value="id"
            v-validate="isNullable(field.title) ? '' : 'required'"
            data-vv-as="selected"
            :class="{ 'red--text': errors.has(field.title + field.object['obj'].id)}"
            :data-vv-name="field.title + field.object['obj'].id"
            solo
            @focus="loadRelated"
            @input="fieldChanged">
        </v-select>
        <span v-show="errors.has(field.title + field.object['obj'].id)" class="red--text">
            {{ errors.collect(field.title + field.object['obj'].id)[0] }}
        </span>
    </v-list-tile-content>
</template>
<script>
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
import mixinAdminFieldRelation from '@/mixins/mixinAdminFieldRelation.vue';
const Vuetify = require("vuetify").default

export default {
    name: 'relatedField',
    inject: ['$validator'],
    mixins: [mixinAdminFieldRelation, mixinAdminField],
    props: ['field'],
    mounted: function() {
        this.$validator.validateAll();
        this.title = this.$props.field.title;
        if (!this.$props.field.object['rel'][this.cutId(this.$props.field.title)])
            return;
        this.relatedObj = [{
                'id': this.$props.field.value,
                'title': this.$props.field.object['rel'][this.cutId(this.$props.field.title)][0]['title']
            }];
        this.relatedObjSelect = _.cloneDeep(this.relatedObj[0]['id']);
        if (!this.relatedObjSelect)
            return;
        console.log("MOUNTED ", this.$validator);
        this.$validator.validateAll();
    },
}
</script>