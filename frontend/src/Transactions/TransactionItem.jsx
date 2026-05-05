
function TransactionItem({transaction}){
    return(
        <div>
            <span>{transaction.symbol}</span>
            <span>{transaction.asset_type}</span>
            <span>{transaction.action}</span>
            <span>{transaction.quantity}</span>
            <span>{transaction.price_of_one}</span>
            <span>{transaction.price_of_one * transaction.quantity}</span>
            {transaction.action === "SELL" && <span>{transaction.profit}</span>}
        </div>
    )
}

export default TransactionItem
