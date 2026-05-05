import { useEffect, useState } from "react";
import { getTransactions } from "../services/api";
import TransactionList from "../Transactions/TransactionList";

function TransactionsPage() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await getTransactions();
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
          {loading && <p>Loading...</p>}{error && <p>{error}</p>}
          <TransactionList transactions={transactions} />

      </div>
  );
}

export default TransactionsPage;
