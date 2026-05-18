import {NavLink} from "react-router-dom";

import '../src/css/Navbar.css'

function NavBar() {
    return (
        <nav className="navbar">
            <div className="navbar-links">
                <NavLink to="/search"
                         className={({isActive}) =>
                             isActive ? "nav-link active" : "nav-link"
                         }>


                    {({isActive}) => (
                        <img className="search" src={
                            isActive
                                ? "../public/assets/search.png"
                                : "../public/assets/search.png"
                        }
                             alt=""
                        />
                    )}
                </NavLink>

                <NavLink to="/Dashboard"
                         className={({isActive}) =>
                             isActive ? "nav-link active" : "nav-link"
                         }>


                    {({isActive}) => (
                        <img className="home" src={
                            isActive
                                ? "../public/assets/home_active.png"
                                : "../public/assets/home.png"
                        }
                             alt=""
                        />
                    )}
                </NavLink>

                <NavLink to="/Transactions"
                         className={({isActive}) =>
                             isActive ? "nav-link active" : "nav-link"
                         }>


                    {({isActive}) => (
                        <img className="transaction" src={
                            isActive
                                ? "../public/assets/transactions_active.png"
                                : "../public/assets/transactions.png"
                        }
                             alt=""
                        />
                    )}
                </NavLink>

                <NavLink to="/holdings"
                         className={({isActive}) =>
                             isActive ? "nav-link active" : "nav-link"
                         }>


                    {({isActive}) => (
                        <img className="holding" src={
                            isActive
                                ? "../public/assets/holdings_active.png"
                                : "../public/assets/holdings.png"
                        }
                             alt=""
                        />
                    )}
                </NavLink>


                <NavLink to="/login"
                         className={({isActive}) =>
                             isActive ? "nav-link active" : "nav-link"
                         }>


                    {({isActive}) => (
                        <img className="profile" src={
                            isActive
                                ? "../public/assets/profile_active.png"
                                : "../public/assets/profile.png"
                        }
                             alt=""
                        />
                    )}
                </NavLink>
            </div>
        </nav>
    )
}

export default NavBar
