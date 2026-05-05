import {useState} from "react";
import {createTransaction} from "../services/api.js";

function TransactionCreate({onClose, onCreated}) {
    const [form, setForm] = useState({
        symbol: "",
        quantity: 0.0,
        price_of_one: 0.0,
        action: "BUY",
        asset_type: ""
    });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        })
    }


    const handleSubmit = async (e) => {
        e.preventDefault();

        await createTransaction({
            ...form,
            quantity: Number(form.quantity),
            price_of_one: Number(form.price_of_one)
        });

        onCreated();
        onClose();
    };


    return (
        <div>
            <h2>Create Transaction</h2>

            <form onSubmit={handleSubmit}>
                <input name="symbol" placeholder="Symbol" onChange={handleChange}/>

                <input name="quantity" type="number" placeholder="Quantity" onChange={handleChange}/>

                <input name="price_of_one" type="number" placeholder="Price" onChange={handleChange}/>

                <select name="action" onChange={handleChange}>
                    <option value="BUY">BUY</option>
                    <option value="SELL">SELL</option>
                </select>

                <button type="submit">Submit</button>
                <button type="button" onClick={onClose}>Cancel</button>
            </form>
        </div>
    );
}

export default TransactionCreate
