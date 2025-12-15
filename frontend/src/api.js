import axios from 'axios';

// In production (Vercel), this comes from Environment Variables.
// In development (local), it defaults to empty string so the Proxy works.
const baseURL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
    baseURL: baseURL,
    timeout: 10000, // Increased timeout for cold starts
});

export default api;
