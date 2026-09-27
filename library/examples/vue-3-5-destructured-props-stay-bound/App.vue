<script setup>
const { count = 0 } = defineProps({ count: Number });
</script>
<template><span class="n">{{ count }}</span></template>
