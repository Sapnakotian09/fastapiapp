import api from "./api";
import type {Company} from "../types/company";

export type CompanyCreatePayload = Omit<Company, "id" | "jobs">;
export type CompanyUpdatePayload = Partial<CompanyCreatePayload>;

export async function getCompanies(): Promise<Company[]> {
    const response = await api.get("/company/");
    return response.data;
}

export async function getCompany(id: number): Promise<Company> {
    const response = await api.get(`/company/${id}`);
    return response.data;
}

export async function createCompany(company: CompanyCreatePayload): Promise<Company> {
    const response = await api.post("/company/", company);
    return response.data;
}

export async function updateCompany(id: number, company: CompanyUpdatePayload): Promise<Company> {
    const response = await api.put(`/company/${id}`, company);
    return response.data;
}

export async function deleteCompany(id: number): Promise<void> {
    const response = await api.delete(`/company/${id}`);
    return response.data;
}