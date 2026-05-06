import {useState} from "react";

function TransactionFilter({onFiltered}) {
    const [form, setForm] = useState({
        symbol: "",
        action: "",
        start_date: "",
        end_date: "",
    })

    const handleChange = async (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        })

    };

    const handleSubmit = async (e) => {
        e.preventDefault()

        onFiltered(form);
    };

    return (
        <div>
            <h2>Filter</h2>

            <form onSubmit={handleSubmit}>
                <input name="symbol" placeholder="Symbol" onChange={handleChange}/>

                <select name="action" onChange={handleChange}>
                    <option value="">ALL</option>
                    <option value="BUY">BUY</option>
                    <option value="SELL">SELL</option>
                </select>

                <div>
                    <label>Start</label>
                    <input
                        type="date"
                        name="start_date"
                        onChange={handleChange}
                    />
                </div>


                <div>
                    <label>End</label>
                    <input
                        type="date"
                        name="end_date"
                        onChange={handleChange}
                    />
                </div>

                <button type="submit">Submit</button>
            </form>
        </div>
    )
}

export default TransactionFilter
