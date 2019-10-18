<template>
    <div class="main">
        <div class="topbar">
            <topbar ref="topbar" />
        </div>
        <div class="search">
            <search ref="search" />
        </div>
        <div class="footer">
            <copyright />
        </div>
    </div>
</template>

<script>

import topbar from '@/components/topbar.vue'
import search from '@/components/search.vue'
import copyright from '@/components/copyright.vue'

export default {
    data() {
        return {
            name: 'main',
            logined: false
        }
    },
    components: {
        topbar: topbar,
        search: search,
        copyright: copyright
    }
}

</script>
