import {Routes, Route} from "react-router-dom"
import NavBar from "./NavBar.jsx";
import TransactionPage from "./pages/TransactionPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import HoldingsPage from "./pages/HoldingsPage.jsx";


function App() {

    return (
        <div>
            <NavBar/>
            <main className="main-content">
                <Routes>
                    <Route path="/Transactions" element={<TransactionPage/>}/>
                    <Route path="/Dashboard" element={<DashboardPage/>}/>
                    <Route path="/Holdings" element={<HoldingsPage/>}/>
                </Routes>
            </main>
        </div>

    )
}


export default App
