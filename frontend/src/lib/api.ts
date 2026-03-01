const API_BASE = "http://localhost:8000/api";

export async function getData(endpoint: string) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("API Error");
  }

  return res.json();
}

export async function postData(endpoint: string, body: any) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function putData(endpoint: string, body: any) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function deleteData(endpoint: string) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "DELETE",
  });
  return res.json();
}