function HoldingsItem({holding}) {
    return (
        <div>
            <span>{holding.symbol}</span>
            <span>{holding.avg_price}</span>
            <span>{holding.quantity}</span>
            <span>{holding.type}</span>
        </div>
    )
}

export default HoldingsItem
