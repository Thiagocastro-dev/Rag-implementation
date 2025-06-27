import { defineStore } from 'pinia';
// Adiciona a nova função do service
import { askQuestion, getDocumentById, searchOrdinances } from '../services/ragService';

export const usePortariaStore = defineStore('portaria', {
  state: () => ({
    // Estado do Chat
    conversation: [], 
    loading: false,
    error: null,
    selectedPortaria: null,

    // --- INÍCIO DA NOVA FUNCIONALIDADE ---
    // Estado da Busca Semântica
    semanticSearchResults: [],
    searchLoading: false,
    searchError: null,
    // --- FIM DA NOVA FUNCIONALIDADE ---
  }),

  getters: {
    latestSources: (state) => {
      const lastAiMessage = [...state.conversation].reverse().find(
        msg => msg.type === 'ai' && msg.sources
      );
      return lastAiMessage ? lastAiMessage.sources : [];
    },
  },

  actions: {
    // Ações do Chat
    async askQuestionRAG(question) {
      this.loading = true;
      this.error = null;
      this.conversation.push({ type: 'user', text: question });
      
      try {
        const response = await askQuestion(question);
        this.conversation.push({ type: 'ai', text: response.answer, sources: response.sources });
      } catch (e) {
        this.error = e.message;
        this.conversation.push({ type: 'error', text: e.message });
      } finally {
        this.loading = false;
      }
    },
      
    async fetchPortariaById(id) {
        this.loading = true; // Pode ser um loading genérico ou um específico
        this.selectedPortaria = null;
        try {
            const portaria = await getDocumentById(id);
            this.selectedPortaria = portaria;
            return portaria;
        } catch (error) {
            this.error = 'Falha ao carregar o conteúdo da portaria.';
            console.error(error);
            return null;
        } finally {
            this.loading = false;
        }
    },
    
    clearSelection() {
        this.selectedPortaria = null;
    },

    // --- INÍCIO DA NOVA FUNCIONALIDADE ---
    // Ação da Busca Semântica
    async performSemanticSearch(query) {
      this.searchLoading = true;
      this.searchError = null;
      this.semanticSearchResults = [];
      try {
        const results = await searchOrdinances(query);
        this.semanticSearchResults = results;
      } catch (e) {
        this.searchError = e.message;
      } finally {
        this.searchLoading = false;
      }
    },
    // --- FIM DA NOVA FUNCIONALIDADE ---
  },
});