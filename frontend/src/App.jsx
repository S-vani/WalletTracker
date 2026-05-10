import {Routes, Route} from "react-router-dom"
import NavBar from "./NavBar.jsx";
import TransactionPage from "./pages/TransactionPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import HoldingsPage from "./pages/HoldingsPage.jsx";
import LoginPage from "./pages/LoginPage.jsx"
import VerifyPage from "./pages/VerifyPage.jsx";
import SignupPage from "./pages/SignupPage.jsx";


function App() {

    return (
        <div>
            <NavBar/>
            <main className="main-content">
                <Routes>
                    <Route path="/Transactions" element={<TransactionPage/>}/>
                    <Route path="/Dashboard" element={<DashboardPage/>}/>
                    <Route path="/Holdings" element={<HoldingsPage/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/verify" element={<VerifyPage/>}/>
                    <Route path="/signup" element={<SignupPage/>}/>
                </Routes>
            </main>
        </div>

    )
}


export default App
