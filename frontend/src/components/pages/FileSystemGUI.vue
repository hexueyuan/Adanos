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
        <div id="right-menu-object" class="right-menu">
            <li @click="handleRename">重命名</li>
            <li @click="handlerDelete">删除</li>
        </div>
        <div id="right-menu-empty"  class="right-menu">
            <li @click="handlerCreateFolder">新建文件夹</li>
            <li @click="handlerCreateFile">新建文件</li>
        </div>
        <el-dialog title="新建文件夹" :visible.sync="newFolderDialogVisible" width="30%">
            <el-input v-model="folderName" placeholder="输入文件夹名"></el-input>
            <div style="margin-top: 20px;">
                <el-button @click="cancleToCreateFolder">取消</el-button>
                <el-button type="primary" @click="ensureToCreateFolder">确定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="新建文件" :visible.sync="newFileDialogVisible" width="30%">
            <el-input v-model="fileName" placeholder="输入文件名"></el-input>
            <div style="margin-top: 20px;">
                <el-button @click="cancleToCreateFile">取消</el-button>
                <el-button type="primary" @click="ensureToCreateFile">确定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="重命名" :visible.sync="renameDialogVisible" width="30%">
            <el-input v-model="newName" placeholder="输入文件名"></el-input>
            <div style="margin-top: 20px;">
                <el-button @click="cancleToRename">取消</el-button>
                <el-button type="primary" @click="ensureToRename">确定</el-button>
            </div>
        </el-dialog>
        <el-dialog title="删除文件(夹)" :visible.sync="deleteDialogVisible" width="30%">
            <div style="margin-top: 20px;">
                <el-button @click="cancleToDelete">取消</el-button>
                <el-button type="primary" @click="ensureToDelete">确定</el-button>
            </div>
        </el-dialog>
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
            lang: 'text',

            newFolderDialogVisible: false,
            folderName: '',
            newFileDialogVisible: false,
            fileName: '',

            renameDialogVisible: false,
            newName: '',
            targetElement: null,

            deleteDialogVisible: false
        }
    },
    mounted () {
        this.request_path_content('/', 'directory')
        this.currentPath = '/'
        var that = this

        var menuEmpty=document.getElementById("right-menu-empty")
        var menuObject=document.getElementById("right-menu-object")
        document.oncontextmenu=function(ev)
        {
            var ev=ev||window.event
            var menu = null
            that.targetElement = ev.toElement
            if (ev.toElement.getAttribute('class') == "item-icon") {
                menu = menuObject
            } else {
                menu = menuEmpty
            }
            var l=ev.clientX
            var t=ev.clientY
            menu.style.display="block"
            menu.style.left=l+'px'
            menu.style.top=t-16+'px'
            return false;
        }
        document.onclick=function()
        {
            menuEmpty.style.display="none"
            menuObject.style.display="none"
        }
    },
    methods: {
        //请求选择元素的内容，封装事件到普通方法的调用
        //    文件夹子文件对象
        //    文本文件的文件内容
        request_select_item_content: function(event) {
            this.request_path_content(event.currentTarget.getAttribute('target'), event.currentTarget.getAttribute('type'))
            return false
        },
        //请求某个路径下的内容
        //    文件夹子文件对象
        //    文本文件的文件内容
        request_path_content: function(path, type) {
            var api = '/apis/fileMonitor'
            var that = this
            this.$axios.get(api + '?' + this.$qs.stringify({path: path})).then(function(res) {
                if (type == 'file') {
                    that.file_content = res.data
                    that.currentIsDir = false
                } else {
                    that.dirItems = res.data
                    that.currentIsDir = true
                }
            }).catch(function() {
                this.alertMessage('服务器数据请求失败', 'error')
            })
        },
        //编辑器初始化函数
        editorInit: function (editor) {
            require('brace/mode/html');
            require('brace/theme/chrome');
            editor.setFontSize(18);
            editor.setOption('readOnly', true)
            editor.resize('100%', '100%')
        },
        //处理点击创建文件夹事件
        handlerCreateFolder: function() {
            this.newFolderDialogVisible = true
        },
        //检查文件夹名称
        //    当前路径下没有重名文件
        //    长度在范围之内  设置长度最大32个字符，比系统本身的规定要小很多
        checkName: function(name) {
            if (name.length > 32 || name.length == 0) {
                return false
            }
            var aim = this.dirItems.find(one => {
                return one.name == name
            })
            if (aim != null) {
                console.log(2)
                return false
            } else {
                return true
            }
        },
        //用户点击创建文件夹确定按钮触发函数
        ensureToCreateFolder: function() {
            if (this.checkName(this.folderName)) {
                var api = '/apis/fileMonitor'
                var argv = {
                    path: this.currentPath + this.folderName,
                    type: 'folder'
                }
                this.$axios.post(api + '?' + this.$qs.stringify(argv)).then(res => {
                    console.log(res.data)
                    if (res.data.result == true) {
                        this.alertMessage('文件夹创建成功', 'success')
                        this.dirItems.push({
                            name: this.folderName,
                            path: this.currentPath + this.folderName,
                            type: 'directory'
                        })
                    } else {
                        this.alertMessage('文件夹创建失败', 'error')
                    }
                }).catch(() => {
                    this.alertMessage('服务器请求失败', 'error')
                })
                this.newFolderDialogVisible = false
            } else {
                this.alertMessage('文件名不合法或者文件名已存在', 'warning')
            }
        },
        //处理点击创建文件夹事件
        handlerCreateFile: function() {
            this.newFileDialogVisible = true
        },
        //用户点击创建文件夹确定按钮触发函数
        ensureToCreateFile: function() {
            if (this.checkName(this.fileName)) {
                var api = '/apis/fileMonitor'
                var argv = {
                    path: this.currentPath + this.fileName,
                    type: 'file'
                }
                this.$axios.post(api + '?' + this.$qs.stringify(argv)).then(res => {
                    if (res.data.result == true) {
                        this.alertMessage('文件创建成功', 'success')
                        this.dirItems.push({
                            name: this.fileName,
                            path: this.currentPath + this.fileName,
                            type: 'file'
                        })
                    } else {
                        this.alertMessage('文件创建失败', 'error')
                    }
                }).catch(() => {
                    this.alertMessage('服务器请求失败', 'error')
                })
                this.newFileDialogVisible = false
            } else {
                this.alertMessage('文件名不合法或者文件名已存在', 'warning')
            }
        },
        //用户点击取消创建文件按钮
        cancleToCreateFile: function() {
            this.newFileDialogVisible = false
        },
        //用户点击取消创建文件夹按钮
        cancleToCreateFolder: function() {
            this.newFolderDialogVisible = false
        },
        handlerDelete: function() {
            this.deleteDialogVisible = true
        },
        cancleToDelete: function() {
            this.deleteDialogVisible = false
        },
        ensureToDelete: function() {
            var api = '/apis/fileMonitor'
            var argv = {
                path: this.currentPath + this.targetElement.getAttribute('name'),
                type: this.targetElement.getAttribute('type')
            }
            this.$axios.delete(api + '?' + this.$qs.stringify(argv)).then(res => {
                if (res.data.result) {
                    var index = this.dirItems.findIndex(one => {
                        return one.name == this.targetElement.getAttribute('name')
                    })
                    this.dirItems.splice(index, 1)
                    this.alertMessage('删除成功', 'success')
                    this.deleteDialogVisible = false
                } else {
                    this.alertMessage('请求服务器失败', 'error')
                }
            })
        },
        handleRename: function() {
            this.renameDialogVisible = true
        },
        ensureToRename: function() {
            if (this.checkName(this.newName)) {
                var api = '/apis/fileMonitor'
                var argv = {
                    path: this.currentPath + this.targetElement.getAttribute('name'),
                    type: 'move'
                }
                var data = {
                    newPath: this.currentPath + this.newName
                }
                this.$axios.put(api + '?' + this.$qs.stringify(argv), data).then(res => {
                    if (res.data.result) {
                        this.alertMessage('重命名成功', 'success')
                        var aim = this.dirItems.find(one => {
                            return one.name == this.targetElement.getAttribute('name')
                        })
                        aim.name = this.newName
                    } else {
                        this.alertMessage('重命名失败', 'error')
                    }
                    this.renameDialogVisible = false
                })
            } else {
                this.alertMessage('名字不合法或名字已存在', 'warning')
            }
        },
        cancleToRename: function() {
            this.renameDialogVisible = false
        },
        //弹窗消息
        alertMessage(msg, type) {
            if (type == "success") {
                this.$message.success(msg)
            } else if (type == "warning") {
                this.$message.warning(msg)
            } else if (type == "error") {
                this.$message.error(msg)
            } else {
                this.$message(msg)
            }
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
.right-menu {
    width:100px; 
    height:80px; 
    padding:10px 3px; 
    background:#5d5d5d; 
    border:#ACA899 1px solid; 
    display:none; 
    position:absolute; 
    left:0;
    top:0;
    border-radius:5px;
    color: #FFFFFF;
    box-shadow:0 0 3px #000;
}
.right-menu li { 
    width:100px; 
    height:30px; 
    line-height:28px; 
    font-size:14px; 
    text-align:center; 
    list-style:none;
}
.right-menu li:hover { 
    background:#316AC5
}
</style>
