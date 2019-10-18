<template>
    <div class="main">
        <el-dialog :visible.sync="visible">
            <div>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: 'changePasswd',
    data() {
        return {
            visible: false
        }
    },
    methods: {
        show() {
            this.visible = true
        }
    }
}
</script>
