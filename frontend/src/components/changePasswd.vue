<template>
    <div class="main">
        <el-dialog :visible.sync="visible">
            <div>
                <h3 style="font-size: 3vh"> 修改密码 </h3>
                <el-input placeholder="请输入管理员密码" v-model="adminPass" show-password/>
                <br><br>
                <el-input placeholder="请输入新的数据库密码" v-model="newPass" show-password/>
                <br><br>
                <el-input placeholder="请再次输入新的数据库密码" v-model="newPassAgain" show-password/>
                <br><br><br>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="visible=false">取消</el-button>
                    <el-button @click="submitChange" type="primary">确定</el-button>
                </span>
            </div>
        </el-dialog>
    </div>
</template>

<script>

import address from '@/address.js'

export default {
    name: 'changePasswd',
    data() {
        return {
            visible: true,
            adminPass: '',
            newPass: '',
            newPassAgain: ''
        }
    },
    methods: {
        show() {
            this.visible = true
        },
        submitChange() {
            if (this.newPass === '' || this.newPass != this.newPassAgain) {
                this.$notify({
                    title: '错误',
                    message: '两次输入的密码不一样或新密码为空'
                })
            }
            let data = {
                adminPass: this.adminPass,
                newPass: this.newPass
            }
            this.$http.post(address.changePasswd, data).then((res) => {
                if (!res.body.result) {
                    this.$notify({title: '错误的管理员密码'})
                } else {
                    this.$notify({title: '修改成功'})
                }
            })
        }
    }
}
</script>
