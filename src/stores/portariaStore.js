import { defineStore } from 'pinia';
import { askQuestion, getDocumentById } from '../services/ragService';

export const usePortariaStore = defineStore('portaria', {
  state: () => ({
    generatedAnswer: null,
    sources: [],
    loading: false,
    error: null,
    selectedPortaria: null,
  }),

  actions: {
    async askQuestionRAG(question) {
      this.loading = true;
      this.error = null;
      this.generatedAnswer = null;
      this.sources = [];
      
      try {
        const response = await askQuestion(question);
        this.generatedAnswer = response.answer;
        this.sources = response.sources;
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    },
      async fetchPortariaById(id) {
        this.loading = true;
        this.selectedPortaria = null; // Limpa a seleção anterior
        try {
            // A API já busca e retorna o documento.
            // Agora, a ação também retorna os dados para o componente que a chamou.
            const portaria = await getDocumentById(id); // Supondo que você tem um serviço para isso
            this.selectedPortaria = portaria;
            return portaria; // MODIFICAÇÃO: Retorna o documento buscado
        } catch (error) {
            this.error = 'Falha ao carregar o conteúdo da portaria.';
            console.error(error);
            return null; // MODIFICAÇÃO: Retorna nulo em caso de erro
        } finally {
            this.loading = false;
        }
    },
    
    async fetchPortariaById(id) {
        this.loading = true;
        this.error = null;
        this.selectedPortaria = null;
        try {
            this.selectedPortaria = await getDocumentById(id);
        } catch (error) {
            this.error = error.message || 'Falha ao carregar o conteúdo da portaria.';
        } finally {
            this.loading = false;
        }
    },
    
    clearSelection() {
        this.selectedPortaria = null;
    }
  },
  
  getters: {
    hasResults: (state) => state.generatedAnswer !== null,
  },
});