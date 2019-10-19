<template>
    <div class="main">
        <el-dialog :visible.sync="visible">
            <div>
                <h3 style="font-size: 3vh"> 添加数据条目 </h3>
                  <el-tabs tab-position="left">
                        <el-tab-pane label="添加文章">
                            <el-input placeholder="期刊" v-model="journal" clearable/> <br> <br>
                            <el-input placeholder="标题" v-model="title" clearable/> <br> <br>
                            <el-input placeholder="内容" v-model="content" type="textarea" :rows="10"/> <br> <br>
                            <el-button @click="uploadArticle" type="primary">上传</el-button>
                        </el-tab-pane>

                        <el-tab-pane label="添加期刊">
                            <h3 style="font-size: 2vh"> 请上传zip压缩文件（可上传多个期刊） </h3>
                            <h3 style="font-size: 2vh"> 文件解压后目录格式为: 期刊号/文章.txt </h3>
                            <el-button @click="uploadJournal" type="primary">上传</el-button>
                        </el-tab-pane>
                    </el-tabs>
            </div>
        </el-dialog>
    </div>
</template>

<script>

import address from '@/address.js'

export default {
    name: 'manage',
    data() {
        return {
            visible: false,
            journal: '',
            content: '',
            title: ''
        }
    },
    methods: {
        show() {
            this.visible = true
        },
        uploadArticle() {
            if (this.article === '' || this.content === '' || this.title === '') {
                this.$notify({
                    title: '错误',
                    message: '期刊、标题或者内容不能留空'
                })
            } else {
                let data = {
                    journal: this.journal,
                    title: this.title,
                    content: this.content
                }
                this.$http.post(address.uploadArticle, data).then((res) => {
                    if (res.body.result) {
                        this.$notify({title: '上传成功'})
                    } else {
                        this.$notify({title: '上传失败'})
                    }
                })
            }
        },
        uploadJournal() {

        }
    }
}
</script>
