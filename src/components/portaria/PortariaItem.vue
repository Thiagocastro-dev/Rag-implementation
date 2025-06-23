<template>
  <q-item>
    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
      <q-item-label caption>Fonte</q-item-label>
    </q-item-section>

    <q-item-section side>
      <q-btn flat round dense icon="visibility" @click="$emit('view', id)" />
    </q-item-section>
  </q-item>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// O componente agora recebe 'id' e 'title' como propriedades
const props = defineProps({
  id: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: 'Título não disponível'
  }
});

defineEmits(['view']);
</script>