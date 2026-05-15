import {useState} from "react";
import TransactionCreate from "./TransactionCreate.jsx";
import {searchStock} from "../services/api.js";
import TransactionSymbolList from "./TransactionSymbolList.jsx";

function TransactionSymbolSearch({onClose, onSub}) {
    const [type, setType] = useState("stock")
    const [symbol, setSymbol] = useState("");
    const [results, setResults] = useState([]);
    const [showSymbols, setShowSymbols] = useState(false)


    const handleChange = (e) => {
        setSymbol(e.target.value)
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (type === "stock"){
            const data = await searchStock(symbol)
            setResults(data)
            setShowSymbols(true)
        }

    };

    return (
        <div>
            <h2>Symbol Search</h2>

            <button onClick={() => setType("stock")}>Stock</button>
            <form onSubmit={handleSubmit}>
                <input name="symbol" placeholder="Symbol" onChange={handleChange}/>

                <button type="submit">Submit</button>
            </form>

            <button onClick={onClose}>Close</button>

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
