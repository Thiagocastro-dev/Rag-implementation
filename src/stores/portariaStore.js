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
      
    // Apenas a versão correta da função é mantida.
    async fetchPortariaById(id) {
        this.loading = true;
        this.selectedPortaria = null; // Limpa a seleção anterior
        try {
            // A API busca e retorna o documento.
            // A ação também retorna os dados para o componente que a chamou.
            const portaria = await getDocumentById(id);
            this.selectedPortaria = portaria;
            return portaria; // Retorna o documento buscado
        } catch (error) {
            this.error = 'Falha ao carregar o conteúdo da portaria.';
            console.error(error);
            return null; // Retorna nulo em caso de erro
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