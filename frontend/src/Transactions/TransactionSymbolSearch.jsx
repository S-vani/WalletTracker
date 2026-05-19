import {useState} from "react";
import {searchCrypto, searchStock} from "../services/api.js";
import TransactionSymbolList from "./TransactionSymbolList.jsx";

function TransactionSymbolSearch({onSub}) {
    const [type, setType] = useState("")
    const [symbol, setSymbol] = useState("");
    const [results, setResults] = useState([]);
    const [showSymbols, setShowSymbols] = useState(false)
    const [loading, setLoading] = useState(false)

    const getPlaceholder = () =>{
        if(type === "stock"){
            return "AAPL, NVDA, GOOG"
        }
        else if (type === "crypto"){
            return "BTC, SOL, ETH"
        }
        else{
            return "Select a type above"
        }
    }


    const handleChange = (e) => {
        setSymbol(e.target.value)
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true)

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
        setLoading(false)

    };

    return (
        <div className="transaction-symbol-wrapper">
            <h2>Search</h2>
            <div className="search-buttons">
                <button
                    className={type === "stock" ? "search-button active" : "search-button"}
                    onClick={() => setType("stock")}>
                    Stock
                </button>
                <button
                    className={type === "crypto" ? "search-button active" : "search-button"}
                    onClick={() => setType("crypto")}>
                    Crypto
                </button>
            </div>
            <form className="symbol-search-form" onSubmit={handleSubmit}>
                <input
                    className="symbol-search-input"
                    name="symbol"
                    placeholder={getPlaceholder()}
                    onChange={handleChange}/>

                <button className="search-button" type="submit">Search</button>
            </form>

            {loading && (
                <h3 className="loading-search">Loading...</h3>
            )}

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
