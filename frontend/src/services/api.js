const BASE_URL = "http://localhost:8000";

function getAuthHeaders() {
    const token = localStorage.getItem("token");

    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

export async function getTransactions(filters = {}) {
    const params = new URLSearchParams()

    if (filters.symbol) {
        params.append("symbol", filters.symbol)
    }
    if (filters.action) {
        params.append("action", filters.action)
    }
    if (filters.start_date) {
        params.append("start_date", new Date(filters.start_date).toISOString())
    }
    if (filters.end_date) {
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
        api_id: String(data.symbol)
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

export async function getDashboardStats(time_span){
    const times = new URLSearchParams()

    if (time_span){
        times.append("current_timeperiod", time_span)
    }

    const url  = times.toString()
        ? `${BASE_URL}/dashboard?${times.toString()}`
        : `${BASE_URL}/dashboard`;

    const res = await fetch(url, {
        headers: getAuthHeaders(),
    })

    if (!res.ok) {
        throw new Error(`Dashboard fetch failed: ${res.status}`);
    }

    return res.json();
}

export async function getHoldings(){

    const res = await fetch(`${BASE_URL}/holdings?}`, {
        headers: getAuthHeaders(),
    });

    if (!res.ok) {
        throw new Error(`Holdings fetch failed: ${res.status}`);
    }

    return res.json();
}

export async function getPriceHistory(symbol, type, range) {
    const res = await fetch(
        `${BASE_URL}/prices/history?symbol=${symbol}&type=${type}&range=${range}`
    );

    if (!res.ok) {
        throw new Error("Failed to load chart data");
    }

    return res.json();
}

export async function getPortfolioHistory(range){
    console.log(range)
    console.log(typeof(range))
    const res = await fetch(
        `${BASE_URL}/portfolio/history?range=${range}`, {
            headers: getAuthHeaders()
        }
    );

    if (!res.ok){
        throw new Error("Failed to load portfolio chart")
    }

    return res.json()
}
