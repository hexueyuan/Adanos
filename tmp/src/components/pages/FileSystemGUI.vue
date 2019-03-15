<template>
    <div id="fileSystem-container">
        <div id="fileSystem-toolbar">
            <button id="fileSystem-backButton" @click="to_back">&lt;</button>
        </div>
        <div style="height: 40px;"></div>
        <div id="fileSystem-contentMain">
            <div id="fileSystem-directory-content" v-if="isDirectory">
                <div v-for="item in file_list" v-bind:key="item.name" class="fileSystem_item_box">
                    <img @dblclick="to_dir(item.path)" :src="item.src" class="fileSystem_item_icon"/>
                    <p class="fileSystem_item_name">{{ item.name }}</p>
                </div>
            </div>
            <div id="fileSystem-file-content" v-if="!isDirectory">
            </div>
        </div>
    </div>
</template>

<script>
const conf = {
    backend_api: 'http://localhost:5000',
    image_path: {
        'directory': '../../static/img/directory.png',
        'python': '../../static/img/python.png',
        'php': '../../static/img/php.png',
        'javascript': '../../static/img/javascript.png',
        'h': '../../static/img/h.png',
        'c': '../../static/img/c.png',
        'c++': '../../static/img/c++.png',
        'html': '../../static/img/html.png',
        'json': '../../static/img/json.png',
        'conf': '../../static/img/conf.png',
        'unknown': '../../static/img/text.png'
    },
    file_type: {
        'py': 'python',
        'php': 'php',
        'js': 'javascript',
        'h': 'h',
        'cpp': 'c++',
        'c': 'c',
        'html': 'html',
        'json': 'json',
        'conf': 'conf'
    }
}
export default {
    data () {
        return {
            history: {
                back: [],
                front: []
            },
            file_list: [],
            isDirectory: true,
            currentPath: '',
            file_content: ''
        }
    },
    mounted () {
        this.isDirectory = true
        var that = this
        this.$http.get(conf['backend_api'] + '/').then(function (response) {
            if (response.data.file_list !== undefined) {
                that.file_list = response.data.file_list
                that.file_list.forEach(element => {
                    if (element.type == "directory") {
                        element.src = conf['image_path']['directory']
                    } else {
                        element.src = conf['image_path'][that.type_by_name(element.name)]
                    }
                });
                that.currentPath = '/'
                that.history.back.push(that.currentPath)
            }
        })
    },
    methods: {
        to_back: function() {
            this.history.front.push(this.history.back.pop())
            this.to_dir(this.history.back.pop())
        },
        to_dir: function (path) {
            var that = this
            console.log(conf['backend_api'] + path)
            this.$http.get(conf['backend_api'] + path).then(function (response) {
                if (response.data.type == 'directory') {
                    that.isDirectory = true
                    if (response.data.file_list !== undefined) {
                        that.file_list = response.data.file_list
                        that.file_list.forEach(element => {
                            if (element.type == "directory") {
                                element.src = conf['image_path']['directory']
                            } else {
                                element.src = conf['image_path'][that.type_by_name(element.name)]
                            }
                        });
                        that.currentPath = path
                        that.history.front = []
                        that.history.back.push(that.currentPath)
                    }
                } else {
                    that.isDirectory = false

                }
            })
        },
        removeChildNodeById: function (id) {
            var el = document.getElementById(id); 
            var childs = el.childNodes; 
            for(var i = childs .length - 1; i >= 0; i--) {
                el.removeChild(childs[i]);
            }
        },
        decoration_element: function (element) {
            var box = document.createElement("div")
            box.setAttribute("class", "file_box")

            var icon = document.createElement('img')
            if (element.type == "file") {
                var type = this.type_by_name(element.name)
                icon.setAttribute("src", conf['image_path'][type])
            } else {
                icon.setAttribute("src", conf['image_path']['directory'])
            }
            icon.setAttribute("class", "filesystem_item_icon")
            icon.setAttribute("data-path", element.path)
            icon.setAttribute("ondblclick", "to_dir(this);return false;")
            
            var text = document.createElement("p")
            text.setAttribute('class', "filesystem_item_name")
            text.innerText = element.name

            box.appendChild(icon)
            box.appendChild(text)
            return box
        },
        type_by_name: function (name) {
            var index1 = name.lastIndexOf('.')
            if (index1 == -1) {
                return "unknown"
            }
            var index2 = name.length
            var suffix = name.substring(index1 + 1, index2)
            if (conf['file_type'][suffix] !== undefined) {
                return conf['file_type'][suffix]
            } else {
                return "unknown"
            }
        }
    }
}
</script>

<style>
#fileSystem-container {
    background-color: #272727;
    height: 100%;
    width: 100%;
    margin: 0px;
    padding: 0px;
    overflow: auto;
}
#fileSystem-toolbar {
    position: fixed ! important;
    background-color: #454545;
    height: 40px;
    width: 100%;
    margin: 0px;
    padding: 0px;
    border-bottom: 0px;
    border-top: 1px;
    border-left: 1px;
    border-right: 1px;
    border-style: solid;
    border-color: #000;
}
#fileSystem-backButton {
    width: 30px;
    height: 30px;
    float: left;
    border: 0px;
    background-color: #666666;
    margin: 5px;
    -webkit-border-radius: 5px;   /* Webkit browsers */
    border-radius:5px;            /* W3C syntax */
    color: aliceblue;
}
.fileSystem_item_icon {
    width: 60px;
    height: 60px;
    padding-top: 10px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 0px;
}
.fileSystem_item_name {
    text-align: center;
    word-wrap: break-word;
    color: aliceblue;
    margin: 0px;
    font-size: 14px;
}
.fileSystem_item_box {
    width: 120px;
    height: 120px;
    float: left;
    text-align:center;
    margin-top: 15px;
}
</style>

