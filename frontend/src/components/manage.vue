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
    name: 'manage',
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
