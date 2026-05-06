import HoldingsItem from "./HoldingsItem.jsx";

function HoldingsList({holdings}) {
    return (
        <div>
            {holdings.map(t => (
                <HoldingsItem key={t.id} holding={t}/>
            ))}
        </div>
    )
}

export default HoldingsList
