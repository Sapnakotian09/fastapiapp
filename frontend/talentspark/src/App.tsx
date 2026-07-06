import { useEffect, useState } from "react";
import NavBar from "./components/NavBar";
import ChatPage from "./pages/chat";
import CompaniesPage from "./pages/companies";
import Login from "./pages/login";
import Register from "./pages/register";
import "./App.css";

type Page = "home" | "chat" | "companies" | "login" | "register";

function App() {
  const [page, setPage] = useState<Page>("home");
  const [token, setToken] = useState<string>(() => localStorage.getItem("token") ?? "");

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  const showHome = () => setPage("home");
  const showChat = () => setPage("chat");
  const showCompanies = () => setPage("companies");
  const showLogin = () => setPage("login");
  const showRegister = () => setPage("register");

  const handleLogin = (newToken: string) => {
    setToken(newToken);
    setPage("home");
  };

  const handleLogout = () => {
    setToken("");
    setPage("home");
  };

  return (
    <div className="app-shell">
      <NavBar
        activePage={page}
        isAuthenticated={Boolean(token)}
        onShowHome={showHome}
        onShowChat={showChat}
        onShowCompanies={showCompanies}
        onShowLogin={showLogin}
        onShowRegister={showRegister}
        onLogout={handleLogout}
      />

      <main className="page-container">
        {page === "home" && (
          <section className="hero">
            <div className="hero-copy">
              <h1>Welcome to TalentSpark</h1>
              <p>Use the navigation above to chat, view companies, or log in.</p>
            </div>

            <div className="hero-card">
              <span className="hero-role">Software Engineer</span>
              <p>Google</p>
              <p>Bangalore</p>
              <p>5 LPA</p>
            </div>
          </section>
        )}

        {page === "chat" && <ChatPage />}
        {page === "companies" && <CompaniesPage />}
        {page === "login" && <Login onLogin={handleLogin} onSwitchToRegister={showRegister} />}
        {page === "register" && <Register onSwitchToLogin={showLogin} />}
      </main>
    </div>
  );
}

export default App;