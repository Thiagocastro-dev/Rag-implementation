import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

/**
 * Envia uma pergunta para a API de RAG e retorna a resposta.
 * @param {string} question - A pergunta do usuário.
 * @returns {Promise<{answer: string, sources: Array<{id: string, title: string}>}>}
 */
export const askQuestion = async (question) => {
  try {
    const response = await apiClient.post('/ask', { question });
    return response.data;
  } catch (error) {
    console.error('Erro ao chamar a API RAG:', error);
    const errorMessage = error.response?.data?.error || 'Não foi possível obter uma resposta. Tente novamente.';
    throw new Error(errorMessage);
  }
};

/**
 * Busca o conteúdo completo de um documento pelo seu ID.
 * @param {string} id - O ID do documento.
 * @returns {Promise<object>} O documento completo.
 */
export const getDocumentById = async (id) => {
  try {
    const response = await apiClient.get(`/document/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar o documento ${id}:`, error);
    throw new Error('Não foi possível carregar o conteúdo da portaria.');
  }
};