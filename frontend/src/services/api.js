
const BASE_URL = "http://localhost:8000";

function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

export async function getTransactions() {
  const res = await fetch(`${BASE_URL}/transactions`, {
    headers: getAuthHeaders(),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch transactions");
  }

  return res.json();
}

export async function createTransaction(data) {
  const res = await fetch(`${BASE_URL}/transactions`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Failed to create transaction");
  }

  return res.json();
}
