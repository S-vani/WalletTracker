import TransactionItem from "./TransactionItem.jsx";

function TransactionList({transactions}) {
    return (
        <div className="transaction-list">
            {transactions.map(t => (
                <TransactionItem key={t.id} transaction={t}/>
            ))}
        </div>
    )
}

export default TransactionList
