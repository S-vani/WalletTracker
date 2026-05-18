import {useState} from "react";
import {searchCrypto, searchStock} from "../services/api.js";
import TransactionSymbolList from "./TransactionSymbolList.jsx";

function TransactionSymbolSearch({onSub}) {
    const [type, setType] = useState("stock")
    const [symbol, setSymbol] = useState("");
    const [results, setResults] = useState([]);
    const [showSymbols, setShowSymbols] = useState(false)


    const handleChange = (e) => {
        setSymbol(e.target.value)
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (type === "stock") {
            const data = await searchStock(symbol)
            setResults(data)
            setShowSymbols(true)
        }
        else if (type === "crypto"){
            const data = await searchCrypto(symbol)
            setResults(data)
            setShowSymbols(true)
        }

    };

    return (
        <div className="transaction-symbol-wrapper">
            <h2>Symbol Search</h2>

            <button onClick={() => setType("stock")}>Stock</button>
            <button onClick={() => setType("crypto")}>Crypto</button>
            <form onSubmit={handleSubmit}>
                <input name="symbol" placeholder="Symbol" onChange={handleChange}/>

                <button type="submit">Submit</button>
            </form>

            {showSymbols && (
                <TransactionSymbolList
                    data={results}
                    onSub={onSub}
                />
            )}
        </div>
    );
}

export default TransactionSymbolSearch
