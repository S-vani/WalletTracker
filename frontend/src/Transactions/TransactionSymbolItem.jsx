function TransactionSymbolItem({data, onSub}) {
    return (
        <div className="transaction-symbol-item-wrapper">
            {data.image !== "" && (
                <img src={data.image} alt="" height={50} width={50}/>
            )}
            <div className="symbol">
                {data.symbol}
            </div>

            <div className="price">
                ${Number(data.price).toFixed(2)}
            </div>

            <div className="type">
                {data.type}
            </div>

            <div className="change">
                <span>${Number(data.change).toFixed(2)}</span>
                <span> ({Number(data.change_pct).toFixed(2)}%)</span>
            </div>

            <button
                className="select-btn"
                onClick={() =>
                    onSub({
                        api_id: data.api_id,
                        symbol: data.symbol,
                        type: data.type
                    })
                }
            >
                Select
            </button>
        </div>
    )
}

export default TransactionSymbolItem
