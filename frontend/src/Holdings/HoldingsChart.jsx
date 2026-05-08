import {useEffect, useState} from "react";
import {getPriceHistory} from "../services/api.js";
import {LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer} from "recharts";

function HoldingChart({symbol, type}) {
    const [range, setRange] = useState("1M");
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const load = async () => {
            setLoading(true);

            const res = await getPriceHistory(symbol, type, range);

            // transform backend → recharts format
            const formatted = res.data.map(p => ({
                time: p.time,
                price: p.price
            }));

            setData(formatted);
            setLoading(false);
        };

        load();
    }, [symbol, range]);

    return (
        <div style={{height: 300}}>
            <div>
                <button onClick={() => setRange("1D")}>1D</button>
                <button onClick={() => setRange("1W")}>1W</button>
                <button onClick={() => setRange("1M")}>1M</button>
                <button onClick={() => setRange("1Y")}>1Y</button>
                <button onClick={() => setRange("5Y")}>5Y</button>
            </div>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time"/>
                        <YAxis/>
                        <Tooltip/>
                        <Line type="monotone" dataKey="price" />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default HoldingChart;
