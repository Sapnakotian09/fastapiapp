import { useEffect, useState } from "react";
import CompanyCard from "../components/CompanyCard";
import type { Company } from "../types/company";
import { getCompanies, createCompany, updateCompany, deleteCompany } from "../Services/CompanyService";

function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadCompanies = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getCompanies();
      setCompanies(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Unable to load companies.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCompanies();
  }, []);

  const handleAdd = async (company: Company) => {
    try {
      await createCompany({
        name: company.name,
        email: company.email,
        phone: company.phone,
        location: company.location,
      });
      await loadCompanies();
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Unable to add company.");
    }
  };

  const handleEdit = async (company: Company) => {
    try {
      await updateCompany(company.id, {
        name: company.name,
        email: company.email,
        phone: company.phone,
        location: company.location,
      });
      await loadCompanies();
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Unable to update company.");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteCompany(id);
      await loadCompanies();
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Unable to delete company.");
    }
  };

  return (
    <section className="page-section companies-page">
      <div className="page-header">
        <h1>Companies</h1>
        <p>View, edit, and manage companies stored in the backend.</p>
      </div>

      {error && <div className="page-error">{error}</div>}
      {loading ? (
        <p>Loading companies...</p>
      ) : (
        <CompanyCard
          companies={companies}
          onadd={handleAdd}
          onedit={handleEdit}
          ondelete={handleDelete}
        />
      )}
    </section>
  );
}

export default CompaniesPage;