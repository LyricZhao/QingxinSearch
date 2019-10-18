<template>
    <div class="main">
        <el-menu :default-active="default_index" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="index"> 清新搜索 </el-menu-item>
            <el-submenu index="submenu">
                <template slot="title"> 管理 </template>
                <el-menu-item index="change"> 更改管理密码 </el-menu-item>
                <el-menu-item index="manage"> 数据词条管理 </el-menu-item>
            </el-submenu>
            <el-menu-item index="about"> 关于 </el-menu-item>
        </el-menu>

        <div>
            <about ref="about"/>
            <changePasswd ref="changePasswd"/>
            <manage ref="manage"/>
        </div>
    </div>
</template>

<script>

import about from '@/components/about.vue'
import changePasswd from '@/components/changePasswd.vue'
import manage from '@/components/manage.vue'

export default {
    name: 'topbar',
    components: {
        about: about,
        changePasswd: changePasswd,
        manage: manage
    },
    data() {
        return {
            default_index: 'index'
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
                case 'manage':
                    this.$refs.manage.show()
                    break
            }
        }
    }
}
</script>
