import {useEffect, useState} from "react";
import {getTransactions} from "../services/api";
import TransactionList from "../Transactions/TransactionList";
import TransactionCreate from "../Transactions/TransactionCreate.jsx"
import TransactionFilter from "../Transactions/TransactionFilter.jsx"
import TransactionSymbolSearch from "../Transactions/TransactionSymbolSearch.jsx";

import '../css/Transaction.css'

function TransactionsPage() {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showSearch, setShowSearch] = useState(false);
    const [showCreate, setShowCreate] = useState(false);
    const [symbolData, setSymbolData] = useState({
        "api_id": "",
        "symbol": "",
        "type": ""
    });

    const loadTransactions = async (filters = {}) => {
        try {
            setLoading(true);
            setError(null);

            const data = await getTransactions(filters);
            setTransactions(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadTransactions();
    }, []);

    return (
        <div>
            <h1 className="page-headers">Transactions</h1>

            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            <TransactionList transactions={transactions}/>

            <div className="filter-add-section">
                <h3>
                    Filters
                </h3>
                <div className="filter-rectangle"></div>
                <TransactionFilter
                    onFiltered={loadTransactions}
                />

                <button className="transaction-button-add" onClick={() => setShowSearch(true)}>
                    Add Transaction
                </button>
            </div>




            {showSearch && (
                <TransactionSymbolSearch
                    onClose={() => setShowSearch(false)}
                    onSub={(data) => {
                        setSymbolData(data)
                        setShowSearch(false);
                        setShowCreate(true);

                    }}
                />
            )}

            {showCreate && (
                <TransactionCreate
                    data={symbolData}
                    onClose={() => setShowCreate(false)}
                    onCreated={loadTransactions}
                />
            )}

        </div>
    );
}

export default TransactionsPage;
