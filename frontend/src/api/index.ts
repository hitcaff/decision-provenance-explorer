const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '') + '/';

async function request(path: string, options?: RequestInit) {
  const url = `${API_BASE}${path.replace(/^\//, '')}`;
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

async function post(path: string, body: unknown) {
  return request(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

// GET /records -> { data: ProvenanceRecord[], total, limit, offset }
export async function fetchRecords() {
  return request('/records');
}

export async function fetchRecord(recordId: string) {
  return request(`/records/${recordId}`);
}

// GET /anchors -> AnchorEvent[] (bare array)
export async function fetchAnchors() {
  return request('/anchors');
}

// GET /anchors/latest -> AnchorEvent | null
export async function fetchLatestAnchor() {
  return request('/anchors/latest');
}

export async function fetchAnchorCount() {
  return request('/anchors/count');
}

// GET /config -> ConfigRecord[] (bare array)
export async function fetchConfigHistory() {
  return request('/config');
}

export async function fetchGenesisHistory() {
  return request('/config/genesis');
}

export async function fetchHealth() {
  return request('/health');
}

export async function fetchEuAiActReport() {
  return request('/records/export/eu_ai_act');
}

export async function verifyChain() {
  return request('/records/verify/chain');
}

export async function initChain(payload: { changed_by: string; reason: string }) {
  return post('/records/init_chain', payload);
}

export async function setConfig(payload: {
  threshold: number;
  above_label: string;
  below_label: string;
  config_version?: string;
  changed_by: string;
  change_reason: string;
}) {
  return post('/records/set_config', payload);
}
