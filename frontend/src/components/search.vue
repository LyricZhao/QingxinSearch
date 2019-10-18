<template>
    <div class="main">
        <div style="margin-top: 15px;">
            <el-input placeholder="搜索内容" v-model="searchText" class="input-with-select" style="width: 95%; margin: 0px auto;">
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
                    <el-table-column prop="content" label="内容"/>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button @click="modifyItem(scope.row)" type="text" size="small"> 查看和修改 </el-button>
                            <el-button @click="deleteItem(scope.row)" type="text" size="small"> 删除 </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                </template>
            <br>
            <el-pagination layout="prev, pager, next" :total="tableData.length" />
        </div>
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

export default {
    name: 'search',
    componenets: {

    },
    data() {
        return {
            tableData: [],
            showResult: true,
            searchText: '清华',
            searchOption: ''
        }
    },
    methods: {
        modifyItem(index) {
        },
        deleteItem(index) {
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
                console.log(res.body.result)
                this.tableData = res.body.result
                if (!tableData.length()) {
                    this.$notify({title: '没有找到搜索结果'})
                }
            })
        }
    }
}

</script>