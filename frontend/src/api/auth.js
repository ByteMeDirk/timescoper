import client from "./client";

export const authApi = {
  register(payload) {
    return client.post("/auth/register/", payload);
  },

  login(email, password) {
    return client.post("/auth/login/", { email, password });
  },

  refreshToken(refresh) {
    return client.post("/auth/token/refresh/", { refresh });
  },

  getMe() {
    return client.get("/auth/me/");
  },

  updateMe(payload) {
    return client.patch("/auth/me/", payload);
  },

  /** Admin endpoints */
  listUsers(params = {}) {
    return client.get("/auth/admin/users/", { params });
  },

  updateUser(userId, payload) {
    return client.patch(`/auth/admin/users/${userId}/`, payload);
  },
};
