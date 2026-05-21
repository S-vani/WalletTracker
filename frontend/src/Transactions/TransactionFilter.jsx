import {useEffect, useState} from "react";

function TransactionFilter({onFiltered}) {
    const [form, setForm] = useState({
        symbol: "",
        action: "",
        start_date: "",
        end_date: "",
    });

    const handleChange = async (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        })

    };

    useEffect(() => {
        onFiltered(form);
    }, [form]);

    return (
        <div className="filter-container">
            <form className="filter-form">

                <div className="filter-group filter-group-symbol">
                    <label className="filter-label">
                        Symbol
                    </label>

                    <input
                        className="filter-input filter-input-symbol"
                        name="symbol"
                        placeholder="AAPL, BTC, TSLA..."
                        onChange={handleChange}
                        autoComplete="off"
                    />
                </div>

                <div className="filter-group filter-group-action">
                    <label className="filter-label">
                        Action
                    </label>

                    <select
                        className="filter-select"
                        name="action"
                        onChange={handleChange}
                        autoComplete="off"
                    >
                        <option value="">ALL</option>
                        <option value="BUY">BUY</option>
                        <option value="SELL">SELL</option>
                    </select>
                </div>

                <div className="filter-group filter-group-date">
                    <label className="filter-label">
                        Start Date
                    </label>

                    <input
                        className="filter-input filter-date-input"
                        type="date"
                        name="start_date"
                        onChange={handleChange}
                        autoComplete="off"
                    />
                </div>

                <div className="filter-group filter-group-date">
                    <label className="filter-label">
                        End Date
                    </label>

                    <input
                        className="filter-input filter-date-input"
                        type="date"
                        name="end_date"
                        onChange={handleChange}
                        autoComplete="off"
                    />
                </div>

            </form>
        </div>
    )
}

export default TransactionFilter
