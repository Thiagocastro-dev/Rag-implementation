`<template>
  <div class="text-center">
    <q-spinner
      :color="color"
      :size="size"
    />
  </div>
</template>

<script setup>
defineProps({
  color: {
    type: String,
    default: 'primary'
  },
  size: {
    type: String,
    default: '3em'
  }
});
</script>`