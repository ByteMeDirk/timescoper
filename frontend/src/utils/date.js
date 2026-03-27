/**
 * Date utility functions for TimeScoper.
 */

export function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function getMonday(date = new Date()) {
  const d = new Date(date);
  const day = d.getDay();
  d.setDate(d.getDate() - ((day + 6) % 7));
  return d;
}

export function toISODate(date) {
  return date.toISOString().split("T")[0];
}

export function getWeekDays(startDate) {
  const monday = getMonday(startDate);
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    return toISODate(d);
  });
}
