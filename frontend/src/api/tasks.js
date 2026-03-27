import client from "./client";

export const tasksApi = {
  list(params = {}) {
    return client.get("/tasks/", { params });
  },

  get(id) {
    return client.get(`/tasks/${id}/`);
  },

  create(payload) {
    return client.post("/tasks/", payload);
  },

  update(id, payload) {
    return client.patch(`/tasks/${id}/`, payload);
  },

  delete(id) {
    return client.delete(`/tasks/${id}/`);
  },

  listComments(taskId) {
    return client.get(`/tasks/${taskId}/comments/`);
  },

  addComment(taskId, body) {
    return client.post(`/tasks/${taskId}/comments/`, { body });
  },
};
