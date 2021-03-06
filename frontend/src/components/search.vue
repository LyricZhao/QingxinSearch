<template>
    <div class="main">
        <div style="margin-top: 15px;">
            <el-input placeholder="搜索内容" v-model="searchText" class="input-with-select" @keyup.enter.native="searchSubmit" style="width: 95%; margin: 0px auto;">
                <el-select v-model="searchOption" slot="prepend" placeholder="搜索选项">
                    <el-option label="关键词" value="keyword" />
                    <el-option label="全文" value="fulltext" />
                    <el-option label="期刊" value="journal" />
                </el-select>
                <el-button @click="searchSubmit" slot="append" icon="el-icon-search" />
            </el-input>
        </div>
        <div>
            <br>
            <template>
                <el-table :data="tableData" border style="width: 95%; margin: 0px auto;">
                    <el-table-column prop="journal" label="期刊"/>
                    <el-table-column prop="title" label="标题"/>
                    <el-table-column prop="brief" label="内容"/>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button v-show="!scope.row.deleted" @click="viewItem(scope.row)" type="text" size="small"> 查看 </el-button>
                            <el-button v-show="!scope.row.deleted" v-if="logined" @click="modifyItem(scope.row)" type="text" size="small"> 修改 </el-button>
                            <el-button v-show="!scope.row.deleted" v-if="logined" @click="deleteItem(scope.row)" type="text" size="small"> 删除 </el-button>
                            <el-tag v-if="logined" v-show="scope.row.deleted" type="danger" size="small"> 已被删除 </el-tag>
                        </template>
                    </el-table-column>
                </el-table>
                </template>
            <br>
            <el-pagination :current-page.sync="currentPage" :page-size="pageSize" @current-change="handlePageChange" layout="prev, pager, next" :total="globalTableData.length" />
        </div>
        <el-dialog width="92%" :visible.sync="modifyVisible">
            <el-input placeholder="期刊" v-model="modifyJournal" clearable/> <br> <br>
            <el-input placeholder="标题" v-model="modifyTitle" clearable/> <br> <br>
            <quill-editor ref="modifyQuillEditor" v-model="modifyContent" :options="modifyOption"/> <br> <br>
            <el-button @click="submitModify" type="primary">修改</el-button>
        </el-dialog>
        <el-dialog width="92%" :visible.sync="viewVisible">
            <el-input placeholder="期刊" v-model="viewJournal"/> <br> <br>
            <el-input placeholder="标题" v-model="viewTitle"/> <br> <br>
            <quill-editor ref="viewQuillEditor" v-model="viewContent" :options="viewOption"/> <br> <br>
        </el-dialog>
    </div>
</template>

<style>
  .el-select .el-input {
    width: 130px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
</style>

<script>

import address from '@/address.js'
import utility from '@/utility.js'

export default {
    name: 'search',
    componenets: {},
    data() {
        return {
            currentPage: 1,
            pageSize: 20,
            tableData: [],
            globalTableData: [],
            showResult: true,
            searchText: '',
            searchOption: '',
            modifyId: -1,
            modifyJournal: '',
            modifyTitle: '',
            modifyContent: '',
            modifyVisible: false,
            modifyIndex: -1,
            viewJournal: '',
            viewTitle: '',
            viewContent: '',
            viewVisible: false,
            maxLength: 200,
            logined: false,
            viewOption: {
                placeholder: '内容',
                readOnly: true
            },
            modifyOption: {
                placeholder: '内容'
            }
        }
    },
    methods: {
        setLogined(logined) {
            this.logined = logined
        },
        viewItem(article) {
            let data = {
                id: article.id
            }
            this.$http.post(address.requestContent, data).then((res) => {
                if (res.body.result) {
                    this.viewJournal = article.journal
                    this.viewTitle = article.title
                    this.viewContent = res.body.content
                    this.viewVisible = true
                } else {
                    this.$notify({title: '获取数据失败'})
                }
            })
        },
        modifyItem(article) {
            let data = {
                id: article.id
            }
            this.$http.post(address.requestContent, data).then((res) => {
                if (res.body.result) {
                    this.modifyId = article.id
                    this.modifyJournal = article.journal
                    this.modifyTitle = article.title
                    this.modifyContent = res.body.content
                    this.modifyVisible = true
                    this.modifyIndex = article.index
                } else {
                    this.$notify({title: '获取数据失败'})
                }
            })
        },
        deleteItem(article) {
            this.$confirm('确认删除？').then(_ => {
                let data = {
                    id: article.id
                }
                this.$http.post(address.deleteArticle, data).then((res) => {
                    if (res.body.result) {
                        this.globalTableData[article.index].deleted = true
                        this.myHandlePageChange(this.currentPage)
                        this.$notify({title: '删除成功'})
                    } else {
                        this.$notify({title: '删除失败', message: '后台可能有任务在执行'})
                    }
                })
                done();
            }).catch(_ => {});
        },
        submitModify() {
            if (this.modifyJournal === '' || this.modifyTitle === '' || this.modifyContent === '') {
                this.$notify({
                    title: '错误',
                    message: '期刊、标题或者内容不能留空'
                })
            } else {
                let data = {
                    index: this.modifyIndex,
                    id: this.modifyId,
                    journal: this.modifyJournal,
                    title: this.modifyTitle,
                    text: this.modifyEditor.getText(),
                    content: this.modifyContent
                }
                this.modifyVisible = false
                this.$http.post(address.modifyArticle, data).then((res) => {
                    if (res.body.result) {
                        this.$notify({title: '修改成功'})
                        this.globalTableData[this.modifyIndex] = res.body.modified
                        this.myHandlePageChange(this.currentPage)
                    } else {
                        this.$notify({title: '修改失败', message: '后台可能有任务在执行'})
                    }
                }).catch(() => {
                    this.$notify({title: '修改失败', message: '后台可能有任务在执行'})
                })
            }
        },
        handlePageChange(currentPage) {
            this.myHandlePageChange(currentPage)
            document.body.scrollTop = document.documentElement.scrollTop = 0
        },
        myHandlePageChange(currentPage) {
            let start = this.pageSize * (currentPage - 1), end = Math.min(this.pageSize * currentPage, this.globalTableData.length)
            this.tableData = []
            for (let i = start; i < end; ++ i)
                this.tableData.push(this.globalTableData[i])
        },
        searchSubmit() {
            if (this.searchText === '') return
            let searchText = this.searchText
            let searchOption = this.searchOption === '' ? 'keyword' : this.searchOption;
            let data = {
                searchText: searchText,
                searchOption: searchOption
            }
            this.$http.post(address.search, data).then((res) => {
                this.globalTableData = res.body.result
                for (let i = 0; i < this.globalTableData.length; ++ i) {
                    this.globalTableData[i].deleted = false
                    this.globalTableData[i].index = i
                }
                this.currentPage = 1
                this.myHandlePageChange(1)
                if (!this.tableData.length) {
                    this.$notify({title: '没有找到搜索结果'})
                }
            })
        }
    },
    computed: {
        modifyEditor() {
            return this.$refs.modifyQuillEditor.quill
        },
        viewEditor() {
            return this.$refs.viewQuillEditor.quill
        }
    }
}

</script>