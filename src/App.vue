`<template>
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
        <div class="q-pa-md">
          <SearchBar />
          <!-- Add PortariasList back to display results -->
          <PortariasList />
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import SearchBar from './components/SearchBar.vue';
import PortariasList from './components/PortariasList.vue'; // Re-added PortariasList import


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


</style>`
