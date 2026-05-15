import TransactionSymbolItem from "./TransactionSymbolItem.jsx";

function TransactionSymbolList({data, onSub}) {
    return (
        <div>
            {data.map(d => (
                <TransactionSymbolItem key={d.api_id} data={d} onSub={onSub}/>
            ))}
        </div>
    )
}

export default TransactionSymbolList
