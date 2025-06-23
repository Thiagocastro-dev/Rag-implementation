<template>
  <div>
    <div v-if="!store.loading && !store.error && store.hasResults">
      <q-card class="bg-grey-1 q-mb-lg" flat bordered>
        <q-card-section>
          <div class="text-h6">Resposta</div>
        </q-card-section>
        <q-separator />
        <q-card-section class="text-body1" style="white-space: pre-wrap;">
          {{ store.generatedAnswer }}
        </q-card-section>
      </q-card>

      <div v-if="store.sources && store.sources.length > 0">
        <div class="text-subtitle2 q-mb-sm">Fontes Consultadas</div>
        <q-list bordered separator>
          <PortariaItem
            v-for="source in store.sources"
            :key="source.id"
            :id="source.id"
            :title="source.title"
            @view="handleShowPortaria" 
          />
        </q-list>
      </div>
    </div>

    <PortariaDialog
      :show="showDialog"
      :portaria="selectedPortaria"
      @close="showDialog = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import PortariaItem from './portaria/PortariaItem.vue';
import PortariaDialog from './portaria/PortariaDialog.vue'; // Certifique-se que o caminho está correto

const store = usePortariaStore();
const showDialog = ref(false);
const selectedPortaria = ref(null);

const handleShowPortaria = async (portariaId) => {
  // Busca os detalhes da portaria na store
  const portariaData = await store.fetchPortariaById(portariaId);
  if (portariaData) {
    selectedPortaria.value = portariaData;
    showDialog.value = true;
  }
};
</script>