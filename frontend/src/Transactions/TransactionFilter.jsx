import { useState } from "react";

function TransactionFilter({ onFilter }) {
  const [symbol, setSymbol] = useState("");
  const [action, setAction] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    onFilter({
      symbol: symbol || undefined,
      action: action || undefined,
      start_date: startDate || undefined,
      end_date: endDate || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Symbol"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />

      <select value={action} onChange={(e) => setAction(e.target.value)}>
        <option value="">All</option>
        <option value="BUY">BUY</option>
        <option value="SELL">SELL</option>
      </select>

      <input
        type="datetime-local"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />

      <input
        type="datetime-local"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />

      <button type="submit">Filter</button>
    </form>
  );
}

export default TransactionFilter;
