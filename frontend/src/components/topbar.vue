<template>
    <div class="main">
        <el-menu :default-active="default_index" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="index"> 清新搜索 </el-menu-item>
            <el-submenu index="submenu">
                <template slot="title"> 管理 </template>
                <el-menu-item index="change" v-show="logined"> 更改管理密码 </el-menu-item>
                <el-menu-item index="addNew" v-show="logined"> 添加数据词条 </el-menu-item>
                <el-menu-item index="status" v-show="logined"> 查看运行状态 </el-menu-item>
                <el-menu-item index="quit" v-show="logined"> 注销 </el-menu-item>
                <el-menu-item index="login"  v-show="!logined"> 登录 </el-menu-item>
            </el-submenu>
            <el-menu-item index="about"> 关于 </el-menu-item>
        </el-menu>

        <el-dialog :visible.sync="loginDialogVisible">
            <h3 style="font-size: 3vh"> 请输入数据库密码 </h3>
            <el-input placeholder="请输入数据库密码" v-model="loginPassword" show-password/> <br> <br>
            <el-button type="primary" @click="submitLogin">确定</el-button>
        </el-dialog>

        <div>
            <about ref="about"/>
            <changePasswd ref="changePasswd"/>
            <addNew ref="addNew"/>
        </div>
    </div>
</template>

<script>

import address from '@/address.js'
import about from '@/components/about.vue'
import changePasswd from '@/components/changePasswd.vue'
import addNew from '@/components/addNew.vue'

export default {
    name: 'topbar',
    components: {
        about: about,
        changePasswd: changePasswd,
        addNew: addNew
    },
    data() {
        return {
            logined: false,
            default_index: 'index',
            loginDialogVisible: false,
            loginPassword: ''
        }
    },
    methods: {
        handleSelect(key) {
            switch (key) {
                case 'about':
                    this.$refs.about.show()
                    break
                case 'change':
                    this.$refs.changePasswd.show()
                    break
                case 'addNew':
                    this.$refs.addNew.show()
                    break
                case 'login':
                    this.loginDialogVisible = true
                    break
                case 'quit':
                    this.logined = false
                    this.$emit('quit')
                    this.$notify({title: '注销成功'})
                case 'status':
                    this.checkStatus()
            }
        },
        checkStatus() {
            this.$http.post(address.runningStatus, {}).then((res) => {
                this.$notify({title: res.body.result ? '正在运行' : '空闲'})
            })
        },
        submitLogin() {
            if (this.loginPassword === '') {
                this.$notify({title: '请不要留空'})
            } else {
                let data = {
                    pass: this.loginPassword
                }
                this.$http.post(address.login, data).then((res) => {
                    if (!res.body.result) {
                        this.$notify({title: '错误的数据库密码'})
                    } else {
                        this.$notify({title: '登录成功'})
                        this.loginDialogVisible = false
                        this.logined = true
                        this.$emit('successLogin')
                    }
                })
            }
        }
    }
}
</script>
