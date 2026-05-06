import {useEffect, useState} from "react";
import {getTransactions} from "../services/api";
import TransactionList from "../Transactions/TransactionList";
import TransactionCreate from "../Transactions/TransactionCreate.jsx"
import TransactionFilter from "../Transactions/TransactionFilter.jsx"

function TransactionsPage() {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showAddForm, setShowAddForm] = useState(false);
    const [showFilterForm, setShowFilterForm] = useState(false)

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
            <h1>Transactions</h1>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            <TransactionList transactions={transactions}/>

            <button onClick={() => setShowAddForm(true)}>
                Add
            </button>
            {showAddForm && (
                <TransactionCreate
                    onClose={() => setShowAddForm(false)}
                    onCreated={loadTransactions}
                />
            )}

            <button onClick={() => setShowFilterForm(true)}>
                Filter
            </button>

            {showFilterForm && (
                <TransactionFilter
                    onFiltered={loadTransactions}

                />

            )}

        </div>
    );
}

export default TransactionsPage;
