<template>
  <div class="chat-container column no-wrap">
    <div class="col-grow chat-messages-area q-pa-md" ref="messagesContainer">
      <div v-for="(message, index) in store.conversation" :key="index">
        <q-chat-message
          :name="message.type === 'user' ? 'Você' : 'Assistente'"
          :sent="message.type === 'user'"
          :bg-color="message.type === 'user' ? 'primary' : 'grey-3'"
          :text-color="message.type === 'user' ? 'white' : 'black'"
          class="q-mb-md"
        >
          <div style="white-space: pre-wrap;">{{ message.text }}</div>
        </q-chat-message>
      </div>
      <div v-if="store.loading" class="row justify-center q-my-md">
        <q-spinner-dots color="primary" size="2em" />
      </div>
       <div v-if="store.error" class="row justify-center q-my-md">
        <q-banner inline-actions class="text-white bg-red">
          {{ store.error }}
        </q-banner>
      </div>
    </div>

    <div class="col-auto chat-input-area">
      <q-separator />
      <div class="q-pa-md">
        <div class="text-overline q-mb-sm">Fazer uma nova pergunta</div>
        <SearchBar />
      </div>
    </div>
    </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import SearchBar from './SearchBar.vue';

const store = usePortariaStore();
const messagesContainer = ref(null);

// Rola para a mensagem mais recente
watch(() => store.conversation, () => {
  nextTick(() => {
    const el = messagesContainer.value;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  });
}, { deep: true });
</script>

<style scoped>
.chat-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  height: calc(100vh - 120px); /* Ajuste a altura conforme necessário */
  display: flex;
  flex-direction: column;
}

.chat-messages-area {
  flex-grow: 1;
  overflow-y: auto;
}

.chat-input-area {
  flex-shrink: 0;
  background-color: #f9f9f9;
}
</style>