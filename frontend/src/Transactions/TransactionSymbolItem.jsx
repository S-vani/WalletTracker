function TransactionSymbolItem({data, onSub}) {
    return (
        <div>
            {data.image !== "" && (
                <img src={data.image} alt="" height={50} width={50}/>
            )}
            <span>{data.api_id}</span>
            <span>{data.symbol}</span>
            <span>{data.type}</span>
            <span>{data.price}</span>
            <span>{data.change}</span>
            <span>{data.change_pct}</span>
            <button onClick={() => onSub({
                "api_id": data.api_id,
                "symbol": data.symbol,
                "type": data.type
            })}>Select
            </button>
        </div>
    )
}

export default TransactionSymbolItem
