import client from "./client";

export const timelogApi = {
  list(params = {}) {
    return client.get("/time-entries/", { params });
  },

  get(id) {
    return client.get(`/time-entries/${id}/`);
  },

  create(payload) {
    return client.post("/time-entries/", payload);
  },

  update(id, payload) {
    return client.patch(`/time-entries/${id}/`, payload);
  },

  delete(id) {
    return client.delete(`/time-entries/${id}/`);
  },

  myLog(date) {
    return client.get("/time-entries/my-log/", { params: { date } });
  },
};
