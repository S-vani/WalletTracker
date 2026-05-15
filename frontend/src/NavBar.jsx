import {Link} from "react-router-dom";

function NavBar() {
    return (
        <nav className="navbar">
            <div className="navbar-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/Transactions" className="nav-link">Transactions</Link>
                <Link to="/Dashboard" className="nav-link">Dashboard</Link>
                <Link to="/login" className="nav-link">Login</Link>
                <Link to="/signup" className="nav-link">Sign up</Link>
            </div>
        </nav>
    )
}

export default NavBar
