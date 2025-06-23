<template>
  <q-input
    filled
    v-model="searchQuery"
    placeholder="Faça uma pergunta sobre as portarias..."
    @keyup.enter="performSearch"
    class="full-width"
    :loading="store.loading"
  >
    <template v-slot:append>
      <q-icon name="search" @click="performSearch" class="cursor-pointer" />
    </template>
  </q-input>
</template>

<script setup>
import { ref } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';

const searchQuery = ref('');
const store = usePortariaStore();

const performSearch = () => {
  if (searchQuery.value.trim()) {
    store.askQuestionRAG(searchQuery.value);
  }
};
</script>