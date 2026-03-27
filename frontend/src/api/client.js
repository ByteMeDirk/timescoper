/**
 * Axios instance with JWT interceptors for the TimeScoper API.
 */
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

/** Inject access token before every request. */
client.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("ts_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/** On 401, attempt a silent token refresh. */
let isRefreshing = false;
let failedQueue = [];

function processQueue(error, token = null) {
  failedQueue.forEach((p) => {
    if (error) {
      p.reject(error);
    } else {
      p.resolve(token);
    }
  });
  failedQueue = [];
}

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return client(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = sessionStorage.getItem("ts_refresh_token");
      if (!refreshToken) {
        isRefreshing = false;
        sessionStorage.removeItem("ts_access_token");
        sessionStorage.removeItem("ts_refresh_token");
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const { data } = await axios.post(`${API_BASE}/api/v1/auth/token/refresh/`, {
          refresh: refreshToken,
        });
        sessionStorage.setItem("ts_access_token", data.access);
        if (data.refresh) {
          sessionStorage.setItem("ts_refresh_token", data.refresh);
        }
        processQueue(null, data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return client(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        sessionStorage.removeItem("ts_access_token");
        sessionStorage.removeItem("ts_refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

export default client;
