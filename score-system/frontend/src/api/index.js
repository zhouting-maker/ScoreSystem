import axios from 'axios';
import { useAuthStore } from '../store/auth';

const api = axios.create({
  baseURL: 'http://localhost:3001/api'
});

api.interceptors.request.use(config => {
  const auth = useAuthStore();
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;
  }
  return config;
});

export const authAPI = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (data) => api.post('/auth/register', data)
};

export const scoreAPI = {
  getScores: () => api.get('/scores'),
  addScore: (data) => api.post('/scores', data),
  getReport: () => api.get('/scores/report'),
  exportExcel: () => api.get('/scores/export', { responseType: 'blob' })
};

export const adminAPI = {
  getUsers: () => api.get('/admin/users'),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
  publishEDU: () => api.post('/admin/publish-edu'),
  getStudents: () => api.get('/admin/students'),
  addStudent: (data) => api.post('/admin/students', data),
  getCourses: () => api.get('/admin/courses'),
  addCourse: (data) => api.post('/admin/courses', data)
};

export const utilsAPI = {
  strlen: (str) => api.post('/utils/strlen', { str })
};

export default api;
