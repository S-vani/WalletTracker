function HoldingsItem({holding}) {
    return (
        <div>
            <span>{holding.symbol}</span>
            <span>{holding.current_price}</span>
            <span>{holding.current_price - holding.price_paid}</span>
            <span>{holding.quantity}</span>
            <span>{holding.type}</span>
        </div>
    )
}

export default HoldingsItem
