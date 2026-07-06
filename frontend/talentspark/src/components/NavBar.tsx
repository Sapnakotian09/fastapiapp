type Props = {
    activePage: "home" | "chat" | "companies" | "login" | "register";
    isAuthenticated: boolean;
    onShowHome: () => void;
    onShowChat: () => void;
    onShowCompanies: () => void;
    onShowLogin: () => void;
    onShowRegister: () => void;
    onLogout: () => void;
};

function NavBar({ activePage, isAuthenticated, onShowHome, onShowChat, onShowCompanies, onShowLogin, onShowRegister, onLogout }: Props) {
    return (
        <nav className="app-nav">
            <ul className="nav-list">
                <li className={`nav-item ${activePage === "home" ? "active" : ""}`} onClick={onShowHome}>Home</li>
                <li className={`nav-item ${activePage === "chat" ? "active" : ""}`} onClick={onShowChat}>Career Chat</li>
                <li className={`nav-item ${activePage === "companies" ? "active" : ""}`} onClick={onShowCompanies}>Companies</li>
                <li className={`nav-item ${activePage === "login" ? "active" : ""}`} onClick={onShowLogin}>Login</li>
                <li className={`nav-item ${activePage === "register" ? "active" : ""}`} onClick={onShowRegister}>Register</li>
            </ul>

            <div className="nav-actions">
                {!isAuthenticated ? (
                    <>
                        <button className="nav-button" type="button" onClick={onShowLogin}>Login</button>
                        <button className="nav-button" type="button" onClick={onShowRegister}>Register</button>
                    </>
                ) : (
                    <button className="nav-button" type="button" onClick={onLogout}>Logout</button>
                )}
            </div>
        </nav>
    );
}

export default NavBar;