<template>
    <div id="file-browser">
        <div v-show="currentIsDir">
            <ul class="list">
                <li v-for="item in dirItems" v-bind:key="item.name" @dblclick="request_select_item_content($event)" :path="item.path" :type="item.type" :name="item.name" class="list-item">
                    <fileItem :type="item.type" :item-name="item.name"/>
                </li>
            </ul>
        </div>
        <div v-show="!currentIsDir" style="height:100%;width:100%">
            <div id="fileSystem-editor-box">
                <editor v-model="file_content" @init="editorInit" theme="chrome" ref="fileEditor" lang="html" id="fileSystem-editor"></editor>
            </div>
        </div>
        <!--右键菜单点击对象时-->
        <div id="right-menu-object" class="right-menu">
            <li @click="renameHandler">重命名</li>
            <li @click="deleteHandler">删除</li>
        </div>
        <!--右键菜单点击空白时-->
        <div id="right-menu-empty"  class="right-menu">
            <li @click="createFolderHandler">新建文件夹</li>
            <li @click="createFileHandler">新建文件</li>
        </div>
        <!--新建文件或者文件夹时的弹窗-->
        <el-dialog title="新建文件(夹)" :visible.sync="create.dialogVisible" width="30%">
            <el-input v-model="create.name" placeholder="输入文件(夹)名"></el-input>
            <div style="margin-top: 30px;">
                <el-button                @click="cancleCreate">取消</el-button>
                <el-button type="primary" @click="ensureCreate">确定</el-button>
            </div>
        </el-dialog>
        <!--重命名文件或者文件夹时的弹窗-->
        <el-dialog title="重命名" :visible.sync="update.dialogVisible" width="30%">
            <el-input v-model="update.name" placeholder="输入文件名"></el-input>
            <div style="margin-top: 30px;">
                <el-button @click="cancleRename">取消</el-button>
                <el-button type="primary" @click="ensureRename">确定</el-button>
            </div>
        </el-dialog>
        <!--删除文件或者文件夹时的弹窗-->
        <el-dialog title="删除文件(夹)" :visible.sync="deleteDialogVisible" width="30%">
            <div style="margin-top: 30px;">
                <el-button @click="cancleDelete">取消</el-button>
                <el-button type="primary" @click="ensureDelete">确定</el-button>
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
            //当前路径是否为文件夹，页面根据该变量切换文件浏览模式和文件编辑模式
            currentIsDir: true,

            //当前路径下的文件对象列表，视图根据该列表进行渲染
            dirItems: [],

            //历史路径窗口，暂未使用
            //historyWindow: [],

            //当前路径，每次跳转之后需要设置该变量
            currentPath: '',

            //编辑器的文本内容，视图使用该变量进行渲染
            file_content: '',

            //编辑器的文本类型，用于代码高亮，暂未使用
            lang: 'text',

            //创建文件(夹)相关数据
            create: {
                name: '',
                mode: '', //mode 标示创建的是文件还是文件夹
                dialogVisible: false
            },

            //重命名
            update: {
                mode: '', //move or update
                name: '',
                dialogVisible: false
            },

            //右键时选中元素
            targetElement: null,

            //删除文件弹窗可视
            deleteDialogVisible: false
        }
    },
    mounted () {
        this.request_path_content('/', 'folder')
        //使能右键菜单
        this.enableRightMenu()
    },
    methods: {
        //============================================================================//
        //============================================================================//
        /* 
         * 页面和相关组件初始化代码
         * enableRightMenu()    使能右键菜单
         * eidtorInit()         Ace编辑器初始化
         */
        //============================================================================//
        //============================================================================//

        // 使能右键菜单
        enableRightMenu: function() {
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

        //Ace eidtor初始化函数
        editorInit: function (editor) {
            require('brace/mode/html');
            require('brace/theme/chrome');
            editor.setFontSize(18);
            editor.setOption('readOnly', true)
            editor.resize('100%', '100%')
        },

        //============================================================================//
        //============================================================================//
        /* 
         * 经常会用到的工具函数
         * checkName()          检查用户提交的名称是否符合规范
         * alertMessage()       在当前页面弹出消息
         */
        //============================================================================//
        //============================================================================//

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
                return false
            } else {
                return true
            }
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
        },

        //============================================================================//
        //============================================================================//
        /* 
         * GET 请求文件夹下子文件对象或者请求文件内容
         * 相关方法封装以及页面触发函数等等
         */
        //============================================================================//
        //============================================================================//

        //请求某个路径下的内容
        //    文件夹子文件对象
        //    文本文件的文件内容
        request_path_content: function(path, type) {
            var api = this.$conf.fileMonitorAPI
            var argv = {path: path, type: type}
            this.$axios.get(api + '?' + this.$qs.stringify(argv)).then(res => {
                if (res.data.result) {
                    if (type == 'file') {
                        this.file_content = res.data.record
                        this.dirItems = []
                        this.currentIsDir = false
                    } else {
                        this.file_content = ''
                        this.dirItems = res.data.record
                        this.currentIsDir = true
                        this.currentPath = path
                    }
                } else {
                    this.alertMessage('接口调用出错：' + res.data.errmsg, 'error')
                }
            }).catch(function() {
                this.alertMessage('服务器数据请求失败', 'error')
            })
        },

        //请求选择元素的内容，封装事件到普通方法的调用
        //    文件夹子文件对象
        //    文本文件的文件内容
        request_select_item_content: function(event) {
            var type = event.currentTarget.getAttribute('type')
            var name = event.currentTarget.getAttribute('name')
            var path = event.currentTarget.getAttribute('path')
            this.request_path_content(path, type)
            
            return false
        },

        //============================================================================//
        //============================================================================//
        /* 
         * POST 请求文件夹下子文件对象或者请求文件内容
         * 相关方法封装以及页面触发函数等等
         */
        //============================================================================//
        //============================================================================//

        //处理点击创建文件夹事件
        createFolderHandler: function() {
            //设置文件夹模式
            this.create.mode = 'folder'
            //打开创建弹窗
            this.create.dialogVisible = true
        },
        //处理点击创建文件事件
        createFileHandler: function() {
            //设置文件夹模式
            this.create.mode = 'file'
            //打开创建弹窗
            this.create.dialogVisible = true
        },
        //用户点击取消创建文件(夹)按钮
        cancleCreate: function() {
            this.create.mode = ''
            this.create.dialogVisible = false
        },
        //用户点击确定创建文件(夹)按钮
        ensureCreate: function() {
            var name = this.create.name
            if (!this.checkName(name)) {
                this.alertMessage('文件名不合法或者文件名已存在', 'warning')
                //直接返回不关闭弹窗
                return
            }

            var api = this.$conf.fileMonitorAPI
            var argv = {
                path: this.currentPath + name,
                type: this.create.mode
            }
            this.$axios.post(api + '?' + this.$qs.stringify(argv)).then(res => {
                if (res.data.result) {
                    //请求成功时，把创建的对象放到当前页面中进行渲染
                    this.dirItems.push({
                        name: name,
                        path: argv.path,
                        type: argv.type
                    })
                    this.alertMessage('文件夹创建成功', 'success')
                } else {
                    this.alertMessage('文件夹创建失败：' + res.data.errmsg, 'error')
                }
            }).catch(() => {
                this.alertMessage('服务器请求失败', 'error')
            })
            //关闭弹窗
            this.create.dialogVisible = false
        },

        //============================================================================//
        //============================================================================//
        /* 
         * PUT 请求文件夹下子文件对象或者请求文件内容
         * 相关方法封装以及页面触发函数等等
         */
        //============================================================================//
        //============================================================================//

        //处理重命名点击事件
        renameHandler: function() {
            this.update.mode = 'move'
            this.update.dialogVisible = true
        },

        //用户点击取消重命名
        cancleRename: function() {
            this.update.mode = ''
            this.update.dialogVisible = false
        },

        //用户确定重命名
        ensureRename: function() {
            var name = this.update.name
            if (!this.checkName(name)) {
                this.alertMessage('文件名不合法或者文件名已存在', 'warning')
                //直接返回不关闭弹窗
                return
            }
            var api = this.$conf.fileMonitorAPI
            var argv = {
                path: this.currentPath + this.targetElement.getAttribute('name'),
                type: 'move'
            }
            var data = {
                newPath: this.currentPath + name
            }
            this.$axios.put(api + '?' + this.$qs.stringify(argv), data).then(res => {
                if (res.data.result) {
                    var aim = this.dirItems.find(one => {
                        return one.name == this.targetElement.getAttribute('name')
                    })
                    aim.name = name
                    this.alertMessage('重命名成功', 'success')
                } else {
                    this.alertMessage('重命名失败：' + res.data.errmsg, 'error')
                }
                this.update.dialogVisible = false
            })
        },

        //============================================================================//
        //============================================================================//
        /* 
         * DELETE 请求文件夹下子文件对象或者请求文件内容
         * 相关方法封装以及页面触发函数等等
         */
        //============================================================================//
        //============================================================================//

        deleteHandler: function() {
            this.deleteDialogVisible = true
        },
        cancleDelete: function() {
            this.deleteDialogVisible = false
        },
        ensureDelete: function() {
            var name = this.targetElement.getAttribute('name')
            var api = this.$conf.fileMonitorAPI
            var argv = {
                path: this.currentPath + name,
                type: this.targetElement.getAttribute('type')
            }
            this.$axios.delete(api + '?' + this.$qs.stringify(argv)).then(res => {
                if (res.data.result) {
                    var index = this.dirItems.findIndex(one => {
                        return one.name == name
                    })
                    this.dirItems.splice(index, 1)
                    this.alertMessage('删除成功', 'success')
                    this.deleteDialogVisible = false
                } else {
                    this.alertMessage('删除失败：' + res.data.errmsg, 'error')
                }
            })
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
