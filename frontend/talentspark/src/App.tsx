import './App.css';
import Welcome from "./components/Welcome";
import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getCompanies } from "./Services/CompanyService";
import type { Company } from "./types/company";

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);

  useEffect(() => {
    void fetchCompanies();
  }, []);

  async function fetchCompanies() {
    setLoading(true);

    try {
      const companies = await getCompanies();
      setCompanies(companies);
    } catch (error: any) {
      setError(error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="status">Loading...</div>;
  }

  if (error) {
    return <div className="status">Error: {error.message}</div>;
  }

  return (
    <div id="center">
      <NavBar />
      <Welcome />
      <JobCard />
      {companies.length > 0 && <CompanyCard companies={companies} />}
      <Footer />
    </div>
  );
}

export default App;
