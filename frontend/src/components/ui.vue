<template>
    <div class="main">
        <div class="topbar">
            <topbar ref="topbar"> </topbar>
        </div>
    </div>
</template>

<script>

import topbar from '@/components/topbar.vue'

export default {
    data() {
        return {
            name: 'main',
            logined: false
        }
    },
    components: {
        topbar: topbar
    }
}

</script>
