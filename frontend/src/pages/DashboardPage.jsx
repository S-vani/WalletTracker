import {useEffect, useState} from "react";
import {getDashboardStats, getTransactions} from "../services/api.js";
import DashboardStats from "../Dashboard/DashboardStats.jsx";
import { useNavigate } from "react-router-dom";


function DashboardPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [stats, setStats] = useState({
        "value": 0.0,
        "curr_timeperiod": 0.0,
    });
    const navigate = useNavigate();

    const loadDashboard = async (time_span) => {
        try {
            setLoading(true);
            setError(null);

            const data = await getDashboardStats(time_span);
            setStats(data)
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDashboard();
    }, []);

    return (
        <div>
            <h1>Dashboard</h1>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            <DashboardStats stats={stats}/>
            <button onClick={() => loadDashboard("day")}>
                1 day
            </button>
            <button onClick={() => loadDashboard("week")}>
                week
            </button>
            <button onClick={() => loadDashboard("month")}>
                month
            </button>
            <button onClick={() => loadDashboard("year")}>
                year
            </button>
            <button onClick={() => loadDashboard()}>
                all time
            </button>
            <button onClick={() => navigate("/Holdings")}>
                holdings
            </button>

        </div>
    )
}

export default DashboardPage
