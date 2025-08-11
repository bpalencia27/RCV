const BASE_API_URL = window.BASE_API_URL || 'http://localhost:8000';
export async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_API_URL}${path}`, {
    headers: { 'Accept': 'application/json', ...(options.headers||{}) },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
