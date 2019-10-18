<template>
    <div class="main">
        <el-dialog :visible.sync="visible">
            <div>
                <el-container>
                    <el-main>
                        <h2 style="font-size: 5vh"> 清新搜索 v1.0 </h2>
                        <br>
                        <el-row style="font-size: 4vh">
                                <el-col :span="12">
                                    <i class="el-icon-loading"> </i> Developer 
                                </el-col>
                                <el-col :span="12">
                                    LyricZ
                                </el-col>
                        </el-row>
                        <el-row style="font-size: 4vh; margin-top: 2%;">
                                <el-col :span="12">
                                    <i class="el-icon-printer"> </i> Frontend
                                </el-col>
                                <el-col :span="12">
                                    Vue/Element
                                </el-col>
                        </el-row>
                        <el-row style="font-size: 4vh; margin-top: 2%;">
                                <el-col :span="12">
                                    <i class="el-icon-setting"> </i> Backend
                                </el-col>
                                <el-col :span="12">
                                    Django/SQLite
                                </el-col>
                        </el-row>
                    </el-main>
                    <br><br><br><br>
                    <el-footer>
                        <el-button type="primary" @click="help" style="font-size: 2vh"> 给作者加鸡腿 </el-button>
                    </el-footer>
                </el-container>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: 'about',
    data() {
        return {
            visible: false
        }
    },
    methods: {
        show() {
            this.visible = true
        },
        help() {
            this.$alert(
                '<img src="/static/images/ui/pay.jpeg" width="100%">',
                '帮助作者',
                {
                    dangerouslyUseHTMLString: true,
                    showConfirmButton: false
                }
            )
        }
    }
}
</script>
