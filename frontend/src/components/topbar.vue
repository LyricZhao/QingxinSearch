<template>
    <div class="main">
        <el-menu :default-active="default_index" class="el-menu-demo" mode="horizontal" v-if="!logined" @select="select">
            <el-menu-item index="index"> 清新搜索 </el-menu-item>
            <el-menu-item index="login"> 登录 </el-menu-item>
            <el-menu-item index="about"> 关于 </el-menu-item>
        </el-menu>
        <el-menu :default-active="default_index" class="el-menu-demo" mode="horizontal" v-if="logined">
            <el-menu-item index="index"> 清新搜索 </el-menu-item>
            <el-submenu index="submenu">
                <template slot="title"> 管理 </template>
                <el-menu-item index="upload"> 上传新期刊 </el-menu-item>
                <el-menu-item index="manage"> 数据库词条管理 </el-menu-item>
            </el-submenu>
            <el-menu-item index="logout"> 注销 </el-menu-item>
            <el-menu-item index="about"> 关于 </el-menu-item>
        </el-menu>

        <div>
            <about ref="about"> </about>
        </div>
    </div>
</template>

<script>

import about from '@/components/about.vue'

export default {
    name: 'topbar',
    components: {
        about: about
    },
    data() {
        return {
            logined: false,
            default_index: 'index'
        }
    },
    methods: {
        select(key) {
            switch (key) {
                case 'about':
                    this.$refs.about.show()
                    break
            }
        }
    }
}
</script>
