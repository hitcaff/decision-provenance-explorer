const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');

async function request(path: string) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || `Request failed: ${res.status}`);
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
