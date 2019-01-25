<template>
    <v-list-tile-content>
        <v-btn outline small color="primary" class="ma-0" @click="loadNtoNRelated">
            {{ntonFormated}}
        </v-btn>
        <v-dialog v-model="displayDialog" content-class="overflow-hidden">
            <v-card>
                <v-card-title>{{ntonFormated}}</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="height: 300px;" scrollable>

                <v-layout>
                    <v-flex xs12 class="scrollable" style="max-height:300px">
                        <v-layout justify-start>
                            <v-flex xs6 offset-md1>
                                <v-autocomplete
                                    v-model="searchElement"
                                    :items="relatedObjNtoN"
                                    item-text="title"
                                    label="Search"
                                    :menu-props="{value:'title'}"
                                    persistent-hint
                                    prepend-icon="mdi-magnify"
                                    append-icon=""
                                />
                            </v-flex>
                        </v-layout>
                        <v-radio-group>
                            <v-layout justify-start v-if="NtonLoadError == 'Nodata'" key="none">   
                                No data for the fields, please finish to fill the database.
                            </v-layout>
                            <v-layout v-else-if="relatedObjNtoN.length == 0" justify-center>
                                <v-progress-circular  :indeterminate="true" color="primary"></v-progress-circular>
                            </v-layout>
                            <v-layout justify-start v-for="item in relatedObjNtoNFiltered()" v-bind:key="item.id">
                                <!-- May bug because of computed property filtered -->
                                <v-flex xs6 md3 offset-md1>
                                    <v-switch
                                        color="primary"
                                        :label="item.title"
                                        :value="item.selected"
                                        v-model="item.selected"
                                        prepend-icon=""
                                        v-on:change="fieldChanged">
                                    </v-switch>
                                </v-flex>
                                <v-flex xs6 md3 offset-md1 v-if="!_.isEmpty(relatedObjNtoNSub)">
                                    <v-select
                                        v-model="item.sub"
                                        :items="relatedObjNtoNSub"
                                        item-text="title"
                                        item-value="id"
                                        :disabled="!item.selected"
                                        solo
                                        @input="fieldChanged">
                                    </v-select>
                                </v-flex>
                            </v-layout>
                        </v-radio-group>
                    </v-flex>
                </v-layout>
                </v-card-text>
                <v-divider></v-divider>
            </v-card>
        </v-dialog>
    </v-list-tile-content>
</template>
<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
import mixinAdminFieldRelation from '@/mixins/mixinAdminFieldRelation.vue';
const Vuetify = require("vuetify").default

export default {
    data() {
        return {
            searchElement: "",
            displayDialog: false,
        }
    },
    name: 'ntonField',
    inject: ['$validator'],
    mixins: [mixinAdminFieldRelation, mixinAdminField],
    props: ['field'],
    computed: {
        ntonFormated: function() {
            return this.relatedNton + 's list';
        },
    },
    methods: {
        applySearch: function(title) {
            if (!this.searchElement || this.searchElement.length == 0)
                return true;
            if (_.toLower(title).includes(_.toLower(this.searchElement)))
                return true;
            return false;
        },
    },
    mounted: function() {
        this.title = this.$props.field.title;
    }
}
</script>