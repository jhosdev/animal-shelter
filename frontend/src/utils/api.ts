import axios from 'axios';
import { getAccessToken, refreshAccessToken, setAuthTokens } from './auth';
import { userAtom } from '@/atoms/userAtom';
import { useAtom } from 'jotai';
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use(
  async (config) => {
    const token = await getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const [user, setUser] = useAtom(userAtom);
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newToken = await refreshAccessToken();
        if (newToken) {
          await setAuthTokens(newToken, null); // Update only the access token
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If token refresh fails, log out the user
        setUser(null);
        await setAuthTokens(null, null);
      }
    }
    return Promise.reject(error);
  }
);

export default api;