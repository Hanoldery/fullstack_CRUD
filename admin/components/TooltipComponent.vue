<template>
    <div style="width: 10px; height: 10px; position: absolute; top: 90vh; left: 90%;">
        <v-tooltip
            fixed
            top
            right
            v-model="this.$store.getters.tooltipSuccess"
            color="green"
            key="tooltipSuccess">

            <div slot="activator"/>
            <v-btn icon>
                <v-icon color="grey lighten-1">mdi-check-all</v-icon>
            </v-btn>
            <span>{{ this.$store.getters.tooltipSuccessMsg }}&nbsp;</span>
        </v-tooltip>
        <v-tooltip
            fixed
            top
            left
            v-model="this.$store.getters.tooltipFail"
            color="red"
            key="tooltipFail">
            <div slot="activator"/>
            <v-btn icon>
                <v-icon color="grey lighten-1">mdi-skull</v-icon>
            </v-btn>
            <span>{{ this.$store.getters.tooltipFailMsg }}&nbsp;</span>
        </v-tooltip>
    </div>
</template>
<script>
export default {
    name: 'TooltipComponent',
}
</script>