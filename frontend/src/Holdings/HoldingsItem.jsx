import HoldingsChart from "./HoldingsChart.jsx"

function HoldingsItem({holding, isOpen, onClick}) {
    return (
        <div>
            <div onClick={onClick}>
                <span>{holding.symbol}</span>
                <span>{holding.current_price}</span>
                <span>{holding.current_price - holding.price_paid}</span>
                <span>{holding.quantity}</span>
                <span>{holding.type}</span>
            </div>

            {isOpen && (
                <div>
                    <HoldingsChart symbol={holding.symbol} type={holding.type}/>
                </div>
            )}
        </div>
    )
}

export default HoldingsItem
