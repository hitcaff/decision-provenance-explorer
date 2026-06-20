const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '') + '/';

async function request(path: string) {
  const url = `${API_BASE}${path.replace(/^\//, '')}`;
  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

export async function fetchRecords() {
  return request('/records');
}

export async function fetchAnchors() {
  return request('/anchors/latest');
}

export async function fetchConfigHistory() {
  return request('/config');
}

export async function fetchHealth() {
  return request('/health');
}
