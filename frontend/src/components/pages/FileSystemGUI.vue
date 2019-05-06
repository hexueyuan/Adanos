<template>
    <div id="file-browser">
        <div v-if="currentIsDir">
            <ul class="list">
                <li v-for="item in dirItems" v-bind:key="item.name" @click="request_select_item_content($event)" :target="item.path" :type="item.type" class="list-item">
                    <fileItem :type="item.type" :item-name="item.name"/>
                </li>
            </ul>
        </div>
        <div v-if="!currentIsDir">
            <div></div>
        </div>
        <context-menu class="right-menu" 
            :target="contextMenuTarget" 
            :show="contextMenuVisible" 
            @update:show="(show) => contextMenuVisible = show">
            <a href="javascript:;">复制</a>
            <a href="javascript:;">引用</a>
            <a href="javascript:;">删除</a>
        </context-menu>
    </div>
</template>

<script>
import fileItem from '@/components/item/fileItem'
import { component as contextMenu } from '@xunlei/vue-context-menu'

export default {
    components: {
        editor: require('vue2-ace-editor'),
        fileItem: fileItem,
        contextMenu: contextMenu
    },
    data () {
        return {
            currentIsDir: true,
            dirItems: [],
            fileContent: '',
            historyWindow: [],
            currentPath: '',
            contextMenuVisible: false,
            contextMenuTarget: null
        }
    },
    mounted () {
        this.request_path_content('/', 'directory')
        this.currentPath = '/'
        window.oncontextmenu = function(e) {
            e.preventDefault()

            this.contextMenuVisible = true
            this.contextMenuTarget = e
        }
    },
    methods: {
        request_select_item_content: function(event) {
            console.log(event.target)
            console.log(event.currentTarget)
            this.request_path_content(event.currentTarget.getAttribute('target'), event.currentTarget.getAttribute('type'))
            return false
        },
        request_path_content: function(path, type) {
            var api = '/apis/fileSystem'
            var that = this
            this.$axios.get(api + '?' + this.$qs.stringify({path: path})).then(function(res) {
                console.log(res)
                if (type == 'file') {
                    that.fileContent = res.data
                    that.currentIsDir = false
                } else {
                    that.dirItems = res.data
                    that.currentIsDir = true
                }
            }).catch(function() {
                console.log("fail to request data")
            })
        }
    }
}
</script>

<style lang="scss">
#file-browser {
    background-color: #ffffff;
    height: 100%;
    width: 100%;
    margin: 0px;
    padding: 0px;
    overflow: auto;
}
#menu {
    position: absolute;
}
.list-item {
    list-style-type:none;
    float: left;
    margin-right: 10px;
    margin-bottom: 10px;
}

   .right-menu {
      border: 1px solid #eee;
      box-shadow: 0 0.5em 1em 0 rgba(0,0,0,.1);
      border-radius: 1px;
      display: block;
      font-family: Microsoft Yahei,Avenir,Helvetica,Arial,sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #2c3e50;
      position: fixed;
      background: #fff;
      border: 1px solid rgba(0,0,0,.2);
      border-radius: 3px;
      z-index: 999;
      display: none;
      a {
        padding: 2px 15px;
 
        // width: 120px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        display: block;
        color: #1a1a1a;
        
      }
      user agent stylesheet
      a:-webkit-any-link {
        color: -webkit-link;
        cursor: pointer;
        text-decoration: underline;
      }
      a:hover {
         background: #42b983;
        //background: $color-primary;
        color: #fff;
      }
   }
</style>
