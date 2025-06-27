<template>
  <div>
    <div v-if="sources.length > 0">
      <div class="text-h6 q-mb-md">Fontes Consultadas</div>
      <q-list bordered separator>
        <PortariaItem
          v-for="source in sources"
          :key="source.id"
          :id="source.id"
          :title="source.title"
          @view="handleShowPortaria" 
        />
      </q-list>
    </div>

    <div v-else-if="!store.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="source" size="4em" />
      <p class="q-mt-md">As fontes da resposta aparecerão aqui.</p>
    </div>

    <PortariaDialog
      v-model="showDialog"
      :portaria="selectedPortaria"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import PortariaItem from './portaria/PortariaItem.vue';
import PortariaDialog from './portaria/PortariaDialog.vue';

const store = usePortariaStore();
const showDialog = ref(false);
const selectedPortaria = ref(null);

// Usa o getter para obter as fontes mais recentes
const sources = computed(() => store.latestSources);

const handleShowPortaria = async (portariaId) => {
  const portariaData = await store.fetchPortariaById(portariaId);
  if (portariaData) {
    selectedPortaria.value = portariaData;
    showDialog.value = true;
  }
};
</script>