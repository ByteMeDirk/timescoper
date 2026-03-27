import client from "./client";

export const projectsApi = {
  list(params = {}) {
    return client.get("/projects/", { params });
  },

  get(id) {
    return client.get(`/projects/${id}/`);
  },

  create(payload) {
    return client.post("/projects/", payload);
  },

  update(id, payload) {
    return client.patch(`/projects/${id}/`, payload);
  },

  delete(id) {
    return client.delete(`/projects/${id}/`);
  },

  getTimeSummary(id) {
    return client.get(`/projects/${id}/time-summary/`);
  },
};
