<template>
  <div>
    <p class="text-body1 q-mb-md">
      Busque as portarias.
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

    <q-list v-if="store.semanticSearchResults.length > 0" bordered separator>
        <q-item-label header>Resultados da Busca</q-item-label>
        <q-item v-for="item in store.semanticSearchResults" :key="item.id" clickable v-ripple @click="handleShowPortaria(item.id)">
            <q-item-section>
                <q-item-label class="text-weight-medium">{{ item.title }}</q-item-label>
                <q-item-label caption lines="2">{{ item.snippet }}</q-item-label>
            </q-item-section>
            <q-item-section side>
                <q-badge :label="`Relevância: ${item.score.toFixed(2)}`" :color="getScoreColor(item.score)" />
            </q-item-section>
        </q-item>
    </q-list>

    <div v-else-if="!store.searchLoading" class="text-center text-grey q-mt-xl">
      <q-icon name="manage_search" size="4em" />
      <p class="q-mt-md"> </p>
    </div>

    <PortariaDialog v-model="showDialog" :portaria="selectedPortaria" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import PortariaDialog from './portaria/PortariaDialog.vue';

const store = usePortariaStore();
const searchQuery = ref('');
const showDialog = ref(false);
const selectedPortaria = ref(null);

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