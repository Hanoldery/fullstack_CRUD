<template>
    <v-container fluid>
        <v-card color="primary" v-if="$store.state.dbStruct" :raised="true" class="elevation-5 mt-5">
            <v-list class="pt-0 primary" dense>
                <v-list-tile>
                    <v-list-tile-content class="display-1 mt-4 ml-3 secondary--text">
                        🎛 Admin Pannel
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
                <v-divider class="my-3"/>
              <v-tabs
                :value="'/' + this.$route.params.object"
                show-arrows
                color="primary"
                dark>
                <v-tabs-slider color="secondary"></v-tabs-slider>

                <v-tab
                  v-for="(value, title, index) in dbStructFilteredWithoutNton"
                  :href="'/' + title"
                  nuxt
                  color="white"
                  :key="title">
                {{ emoji[index] + title | startCase}}
                </v-tab>
              </v-tabs>
            <nuxt-child/>
        </v-card>
    </v-container>
</template>
<script>
import Vue from 'vue';

export default {
    // TODO: Make emoji more flexible, inside JSON or something
    data() {
        return {
            emoji: [
                '🧔',
                '🛠',
                '🕹',
                '📔',
                '📚',
                '🚂',
                '👮‍♂️',
                '💪',
            ]
        }
    },
    methods: {
        filterObjectRejectString(object, stringToReject) {
            if (this._.isEmpty(object))
                return {};
            return Object.keys(object)
                .filter(key => !this._.includes(key, stringToReject))
                .reduce(
                    (obj, key) => {
                        obj[key] = object[key];
                        return obj;
                    }, {}
                );
        }
    },
    computed: {
        dbStructFilteredWithoutNton: function() {
            return this.filterObjectRejectString(this.$store.state.dbStruct, "nton");
        }
    }
};

</script>
