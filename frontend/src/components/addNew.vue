<template>
    <div class="main">
        <el-dialog width="92%" :visible.sync="visible">
            <div>
                <h3 style="font-size: 3vh"> 添加数据条目 </h3>
                  <el-tabs tab-position="left">
                        <el-tab-pane label="添加文章">
                            <el-input placeholder="期刊" v-model="journal" clearable/> <br> <br>
                            <el-input placeholder="标题" v-model="title" clearable/> <br> <br>
                            <quill-editor ref="quillEditor" v-model="content" :options="quillOption"/> <br> <br>
                            <el-button @click="uploadArticle" type="primary">上传</el-button>
                        </el-tab-pane>

                        <el-tab-pane label="添加期刊">
                            <el-upload drag :on-success="uploadJournalSuccess" :on-error="uploadJournalError" :action="uploadJournalAddress" :show-file-list="false">
                                <i class="el-icon-upload"></i>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                <div class="el-upload__tip" slot="tip">请上传zip压缩文件（可上传多个期刊，文件解压后目录格式为: 期刊号/文章.txt）</div>
                            </el-upload>
                        </el-tab-pane>
                    </el-tabs>
            </div>
        </el-dialog>
    </div>
</template>

<script>

import address from '@/address.js'
import utility from '@/utility.js'

export default {
    name: 'manage',
    data() {
        return {
            visible: false,
            journal: '',
            content: '',
            title: '',
            uploadJournalAddress: address.uploadJournal,
            quillOption: {
                placeholder: '内容'
            }
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
                    content: this.content,
                    text: this.editor.getText()
                }
                this.$http.post(address.uploadArticle, data).then((res) => {
                    if (res.body.result) {
                        this.$notify({title: '上传成功'})
                        this.visible = false;
                        this.journal = ''
                        this.content = ''
                        this.title = ''
                    } else {
                        this.$notify({title: '上传失败'})
                    }
                })
            }
        },
        uploadJournalSuccess() {
            this.$notify({title: '上传成功', message: '任务已经提交到后台，可能需要一段时间，请耐心等待'})
            this.visible = false
        },
        uploadJournalError() {
            this.$notify({title: '上传失败', message: '后台可能有任务在执行'})
        }
    },
    computed: {
        editor() {
            return this.$refs.quillEditor.quill
        }
    },
}
</script>
