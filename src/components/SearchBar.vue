<template>
  <q-input
    filled
    v-model="searchQuery"
    placeholder="Faça uma pergunta sobre as portarias..."
    @keyup.enter="performSearch"
    class="full-width"
    :loading="store.loading"
    :disable="store.loading"
  >
    <template v-slot:append>
      <q-btn dense flat round icon="send" @click="performSearch" :disable="store.loading" />
    </template>
  </q-input>
</template>

<script setup>
import { ref } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';

const searchQuery = ref('');
const store = usePortariaStore();

const performSearch = () => {
  if (searchQuery.value.trim() && !store.loading) {
    store.askQuestionRAG(searchQuery.value);
    searchQuery.value = ''; // Limpa o input após o envio
  }
};
</script>