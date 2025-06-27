<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-img
          src="src/assets/logo-mpc.png"
          spinner-color="white"
          style="height: 40px; max-width: 180px"
          fit="contain"
          class="q-mr-md"
        />
        <q-toolbar-title>
          Busca de Portarias MPC
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>

        <q-tabs v-model="tab" dense class="text-grey" active-color="primary" indicator-color="primary" align="left" narrow-indicator>
          <q-tab name="chat" icon="Youtube" label="Chat com Documentos" />
          <q-tab name="search" icon="travel_explore" label="Busca Semântica" />
        </q-tabs>
        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="chat" class="q-pa-none q-pt-md">
            <div class="row q-col-gutter-lg">
              <div class="col-12 col-md-8">
                <Chat />
              </div>
              <div class="col-12 col-md-4">
                <PortariasList />
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel name="search" class="q-pa-none q-pt-md">
            <SemanticSearch />
          </q-tab-panel>
        </q-tab-panels>
        </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue';
import Chat from './components/Chat.vue';
import PortariasList from './components/PortariasList.vue';
// Importa o novo componente
import SemanticSearch from './components/SemanticSearch.vue'; 

const tab = ref('chat');
</script>

<style>
.q-toolbar {
  min-height: 64px;
}

.q-img {
  transition: transform 0.2s;
}

.q-img:hover {
  transform: scale(1.05);
}
</style>