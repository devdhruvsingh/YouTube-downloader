import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeVideo = async (url) => {
  const response = await api.post('/download/analyze/', { url });
  return response.data;
};

export const startDownload = async (url, formatId) => {
  const response = await api.post('/download/process', { url, format_id: formatId });
  return response.data;
};

export const getDownloadStatus = async (taskId) => {
  const response = await api.get(`/download/status/${taskId}`);
  return response.data;
};

export const getFileDownloadUrl = (taskId) => {
  return `${API_BASE_URL}/download/file/${taskId}`;
};

export default api;