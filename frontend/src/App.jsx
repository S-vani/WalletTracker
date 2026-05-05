import {Routes, Route} from "react-router-dom"
import NavBar from "./NavBar.jsx";
import TransactionPage from "./pages/TransactionPage.jsx";

function App() {

    return (
        <div>
            <NavBar/>
            <main className="main-content">
                <Routes>
                    <Route path="/Transactions" element={<TransactionPage/>}/>
                </Routes>
            </main>
        </div>

    )
}


export default App
