
const BASE_URL = "http://localhost:8000";

function getAuthHeaders() {
    const token = localStorage.getItem("token");

    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

export async function getTransactions(filters ={}) {
    const params = new URLSearchParams()

    if (filters.symbol){
        params.append("symbol", filters.symbol)
    }
    if (filters.action){
        params.append("action", filters.action)
    }
    if (filters.start_date){
        params.append("start_date", new Date(filters.start_date).toISOString())
    }
    if (filters.end_date){
        params.append("end_date", new Date(filters.end_date).toISOString())
    }



    const res = await fetch(`${BASE_URL}/transactions?${params.toString()}`, {
        headers: getAuthHeaders(),
    });

    if (!res.ok) {
        throw new Error("Failed to fetch transactions");
    }

    return res.json();
}

export async function createTransaction(data) {

    data = {
        ...data,
        api_id:"bitcoin"
    }

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
