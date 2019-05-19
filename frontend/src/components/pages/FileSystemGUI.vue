<template>
    <div id="file-browser">
        <div v-show="currentIsDir">
            <ul class="list">
                <li v-for="item in dirItems" v-bind:key="item.name" @click="request_select_item_content($event)" :target="item.path" :type="item.type" class="list-item">
                    <fileItem :type="item.type" :item-name="item.name"/>
                </li>
            </ul>
        </div>
        <div v-show="!currentIsDir" style="height:100%;width:100%">
            <div id="fileSystem-editor-box">
                <editor v-model="file_content" @init="editorInit" theme="chrome" ref="fileEditor" lang="html" id="fileSystem-editor"></editor>
            </div>
        </div>
    </div>
</template>

<script>
import fileItem from '@/components/item/fileItem'

export default {
    components: {
        editor: require('vue2-ace-editor'),
        fileItem: fileItem
    },
    data () {
        return {
            currentIsDir: true,
            dirItems: [],
            historyWindow: [],
            currentPath: '',
            contextMenuVisible: false,
            contextMenuTarget: null,
            file_content: '',
            lang: 'text'
        }
    },
    mounted () {
        this.request_path_content('/', 'directory')
        this.currentPath = '/'
    },
    methods: {
        request_select_item_content: function(event) {
            this.request_path_content(event.currentTarget.getAttribute('target'), event.currentTarget.getAttribute('type'))
            return false
        },
        request_path_content: function(path, type) {
            var api = '/fileMonitor'
            var that = this
            this.$axios.get(api + '?' + this.$qs.stringify({path: path})).then(function(res) {
                if (type == 'file') {
                    that.file_content = res.data
                    console.log(that.file_content)
                    that.currentIsDir = false
                } else {
                    that.dirItems = res.data
                    that.currentIsDir = true
                }
            }).catch(function() {
                console.log("fail to request data")
            })
        },
        editorInit: function (editor) {
            require('brace/mode/html');
            require('brace/theme/chrome');
            //let editor = this.$refs.fileEditor.editor
            editor.setFontSize(18);
            editor.setOption('readOnly', true)
            editor.resize('100%', '100%')
        }
    }
}
</script>

<style lang="scss">
#file-browser {
    background-color: #FFFFFF;
    height: 100%;
    width: 100%;
    margin: 0px;
    padding: 0px;
    overflow: auto;
}
.list-item {
    list-style-type:none;
    float: left;
    margin-right: 10px;
    margin-bottom: 10px;
}
#fileSystem-editor-box {
    height: 100%;
    width: 100%;
}
#fileSystem_editor {
    width: 100%;
    height: 100%;
}
</style>
