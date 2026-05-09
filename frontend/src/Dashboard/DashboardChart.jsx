import {useEffect, useState} from "react";
import {getPortfolioHistory} from "../services/api.js";
import {LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer} from "recharts";

function DashboardChart() {
    const [range, setRange] = useState(1);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    const loadDashboardChart = async (selectedRange) => {
        setLoading(true);
        const res = await getPortfolioHistory(selectedRange);

        // res is the array directly from FastAPI, each item: { time, value }
        setData(res);
        setLoading(false);
    };

    useEffect(() => {
        loadDashboardChart(range);
    }, [range])

    return (
        <div style={{height: 300}}>
            <div>
                <button onClick={() => setRange(1)}>1D</button>
                <button onClick={() => setRange(7)}>1W</button>
                <button onClick={() => setRange(31)}>1M</button>
                <button onClick={() => setRange(365)}>1Y</button>
            </div>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time"/>
                        <YAxis/>
                        <Tooltip/>
                        <Line type="monotone" dataKey="value"/>
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default DashboardChart;
