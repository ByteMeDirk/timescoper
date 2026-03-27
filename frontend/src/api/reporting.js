import client from "./client";

export const reportingApi = {
  dailySummary(params = {}) {
    return client.get("/reports/daily-summary/", { params });
  },

  weeklySummary(params = {}) {
    return client.get("/reports/weekly-summary/", { params });
  },

  projectUtilisation(projectId) {
    return client.get("/reports/project-utilisation/", {
      params: { project_id: projectId },
    });
  },

  teamActivity(params = {}) {
    return client.get("/reports/team-activity/", { params });
  },
};
