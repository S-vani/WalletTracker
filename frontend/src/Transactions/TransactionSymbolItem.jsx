function TransactionSymbolItem({data, onSub}) {
    const change = data.change < 0 ? -data.change : data.change
    const pct = data.change_pct > 0 ? "+" + data.change_pct.toFixed(2) : data.change_pct.toFixed(2).toString()

    return (
        <div className="transaction-symbol-item-wrapper">

            <div className="symbol">
                <span className="symbol-image">
                    {
                        data.image !== "" && (
                            <img src={data.image} alt=""/>
                        )}
                </span>

                <span className="symbol-text">{data.symbol}</span>
            </div>

            <div className="price">
                ${Number(data.price).toFixed(3)}
            </div>

            <div className="type">
                {data.type}
            </div>

            <div className="change">
                <span className={data.change < 0 ? "change-number negative" : "change-number positive"}>
                    ${Number(change).toFixed(3)}
                </span>

                <span>(</span>
                <span className={data.change_pct < 0 ? "change-pct negative" : "change-pct positive"}>
                    {pct}%
                </span>
                <span>)</span>
            </div>

            <button
                className="select-btn"
                onClick={() =>
                    onSub({
                        api_id: data.api_id,
                        symbol: data.symbol,
                        type: data.type
                    }, data)
                }
            >
                Select
            </button>
        </div>
    )
}

export default TransactionSymbolItem
