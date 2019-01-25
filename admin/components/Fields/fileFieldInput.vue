<template>
    <form
        :id="'upload_form' + field.object['obj'].id + field.index"
        role="form"
        enctype="multipart/form-data"
        method="POST"
        class="hover-trigger"
        style="width: 100%; height:100%;">
        <input
            type="file"
            :ref="'ref' + this.field.title + this.field.object['obj'].id"
            :name="field.title + field.object['obj'].id"
            :id="field.title + field.object['obj'].id"
            style="display: none"
            v-on:change="onFileChange"
            :accept="fileType + '/*'"
            class="form-control"/>
            <img v-if="fileType == 'image'"
                :src="imageUrlFormated"
                :lazy-src="imageUrlFormated"
                aspect-ratio="1"
                fill-height
                class="grey lighten-2"/>
            <div @click="pickFile" class="hover-overlay">
                <span v-if="fileType != 'image'">
                    Pick a {{ fileType }}
                </span>
            </div>
    </form>
</template>
<script> 
import Vue from 'vue';
import mixinAdminField from '@/mixins/mixinAdminField.vue';
const Vuetify = require("vuetify").default

export default {
    name: 'fileFieldInput',
    props: ['field', 'fileType'],
    mixins: [mixinAdminField],
    computed: {
        imageUrlFormated: function() {
            var img;
            try {
                img = require('@/static/img/' + this.field.value);
            }
            catch (error) {
                console.log("⚠️ 📸 Image not found :", error);
                try {
                    img = require('@/static/img/' + this.$route.params.object + '/default.png');
                }
                catch (error) {
                    img = require('@/static/img/ze.png');
                }
            }
            return img;
        },
    },
    methods: {
        pickFile: function() {
            this.$refs['ref' + this.field.title + this.field.object['obj'].id].click();
        },
        onFileChange(e) {
            let files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.createFile(files[0]);
        },
        extractFileExtension: function() {
            return _.split(
                document.getElementById(
                    this.field.title +
                    this.field.object['obj'].id
                ).files[0].name,
                '.'
            )
        },
        extractFileData: function() {
            return document.getElementById(
                this.field.title +
                this.field.object['obj'].id
            ).files[0]
        },
        createFile(file) {
            let reader = new FileReader();
            var data = new FormData();
            let _vm = this;
            reader.onload = (e) => {
                _vm.imageData = e.target.result;
                var extension = _vm.extractFileExtension()
                extension = extension[extension.length - 1];

                if (extension.length < 1)
                    return;

                data.append('file', _vm.extractFileData());
                data.append('field_name', _vm.field.object['obj'].id.toString() + _vm.field.index.toString());
                _vm.$axios.$post(
                  '/upload/' +
                  _vm.$route.params.object + '/' +
                  _vm.field.object['obj'].id, data)
                    .then(function (response) {
                        _vm.fieldChanged(
                            _vm.$route.params.object +
                            '/' + _vm.$route.params.object +
                            '_' + _vm.field.object['obj'].id +
                            _vm.field.object['obj'].id.toString() +
                            _vm.field.index.toString() +
                            '.' + extension
                        )   
                    });
            };
            reader.readAsDataURL(file);
        },
    }
}
</script>