import axios from 'axios';

const api = axios.create({
    // baseURL removed to rely on relative paths (Vite Proxy)
    timeout: 5000,
});

export default api;
