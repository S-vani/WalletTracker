import HoldingsItem from "./HoldingsItem.jsx";
import {useState} from "react";

function HoldingsList({holdings}) {
    const [selectedSymbol, setSelectedSymbol] = useState(null);

    return (
        <div>
            {holdings.map(t => (
                <HoldingsItem
                    key={t.id}
                    holding={t}
                    isOpen={selectedSymbol === t.symbol}
                    onClick={() => setSelectedSymbol(t.symbol)}/>
            ))}
        </div>
    )
}

export default HoldingsList
