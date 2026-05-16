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
        <div>
            <form className="filter-form">
                <input className="filter-form-symbol" name="symbol" placeholder="Symbol" onChange={handleChange}/>

                <select name="action" onChange={handleChange}>
                    <option value="">ALL</option>
                    <option value="BUY">BUY</option>
                    <option value="SELL">SELL</option>
                </select>

                <div>
                    <label className="filter-form-date-start">Start</label>
                    <input
                        type="date"
                        name="start_date"
                        onChange={handleChange}
                    />
                </div>


                <div>
                    <label className="filter-form-date-end">End </label>
                    <input
                        type="date"
                        name="end_date"
                        onChange={handleChange}
                    />
                </div>
            </form>
        </div>
    )
}

export default TransactionFilter
