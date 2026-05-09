import {useEffect, useState} from "react";
import {getHoldings} from "../services/api.js";
import HoldingsList from "../Holdings/HoldingsList.jsx";


function HoldingsPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [holdings, setHoldings] = useState([]);

    const loadHoldings = async () => {
        try {
            setLoading(true);
            setError(null);

            const data = await getHoldings();
            setHoldings(data)
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHoldings();
    }, []);

    return (
        <div>
            <HoldingsList holdings={holdings}/>

        </div>
    )
}

export default HoldingsPage
