import axios from 'axios';
import { COUCHDB_CONFIG } from '../config/couchdb';

export const createApiClient = () => {
  return axios.create({
    baseURL: COUCHDB_CONFIG.url,
    auth: {
      username: COUCHDB_CONFIG.username,
      password: COUCHDB_CONFIG.password
    },
    headers: {
      'Content-Type': 'application/json'
    }
  });
};

export const handleApiError = (error) => {
  if (error.response) {
    throw new Error(`Erro do servidor: ${error.response.status}`);
  } else if (error.request) {
    throw new Error('Erro de conexão com o servidor');
  }
  throw new Error('Erro ao processar requisição');
};