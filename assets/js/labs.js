import { apiFetch } from './api.js';
export async function autofill(file){
  const fd = new FormData(); fd.append('file', file);
  const data = await fetch('http://localhost:8000/api/upload', { method:'POST', body: fd}).then(r=>r.json());
  return data;
}
