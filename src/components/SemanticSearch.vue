<template>
  <div>
    <p class="text-body1 q-mb-md">
      Busque por um tema ou assunto para encontrar as portarias mais relevantes.
    </p>
    <q-input
      filled
      v-model="searchQuery"
      label="Digite um assunto ou tema para a busca..."
      @keyup.enter="runSearch"
      class="q-mb-lg"
      :loading="store.searchLoading"
      :disable="store.searchLoading"
    >
      <template v-slot:append>
        <q-btn dense flat round icon="search" @click="runSearch" :disable="store.searchLoading" />
      </template>
    </q-input>

    <div v-if="store.searchError" class="q-my-md">
       <q-banner inline-actions class="text-white bg-red">
          {{ store.searchError }}
        </q-banner>
    </div>

    <q-list v-if="paginatedResults.length > 0" bordered separator>
        <q-item-label header>Resultados da Busca ({{ store.semanticSearchResults.length }})</q-item-label>
        <q-item v-for="item in paginatedResults" :key="item.id" clickable v-ripple @click="handleShowPortaria(item.id)">
            <q-item-section>
                <q-item-label class="text-weight-medium">{{ item.title }}</q-item-label>
                <q-item-label caption lines="2">{{ item.snippet }}</q-item-label>
            </q-item-section>
            <q-item-section side>
                <q-badge :label="`Relevância: ${item.score.toFixed(2)}`" :color="getScoreColor(item.score)" />
            </q-item-section>
        </q-item>
    </q-list>

    <div v-if="totalPages > 1" class="flex flex-center q-mt-lg">
        <q-pagination
            v-model="currentPage"
            :max="totalPages"
            direction-links
        />
    </div>

    <div v-else-if="!store.searchLoading" class="text-center text-grey q-mt-xl">
      <q-icon name="manage_search" size="4em" />
      <p class="q-mt-md">Nenhum resultado para exibir. Realize uma busca para começar.</p>
    </div>

    <PortariaDialog v-model="showDialog" :portaria="selectedPortaria" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import PortariaDialog from './portaria/PortariaDialog.vue';

const store = usePortariaStore();
const searchQuery = ref('');
const showDialog = ref(false);
const selectedPortaria = ref(null);

// Estado para a paginação
const currentPage = ref(1);
const itemsPerPage = ref(10);

const totalPages = computed(() => {
    return Math.ceil(store.semanticSearchResults.length / itemsPerPage.value);
});

const paginatedResults = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return store.semanticSearchResults.slice(startIndex, endIndex);
});

const runSearch = () => {
    if (searchQuery.value.trim()) {
        store.performSemanticSearch(searchQuery.value);
    }
}

const handleShowPortaria = async (portariaId) => {
  const portariaData = await store.fetchPortariaById(portariaId);
  if (portariaData) {
    selectedPortaria.value = portariaData;
    showDialog.value = true;
  }
};

const getScoreColor = (score) => {
    if (score > 0.82) return 'positive';
    if (score > 0.75) return 'orange';
    return 'grey-7';
}
</script>