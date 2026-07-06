import { useState, type FormEvent } from "react";
import { register } from "../Services/AuthService";

type Props = {
    onSwitchToLogin: () => void;
};

function Register({ onSwitchToLogin }: Props) {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await register({ name, email, password, role });
            alert("Registration successful! Please login.");
            onSwitchToLogin();
        } catch (error) {
            console.error("Error during registration:", error);
            alert("Registration failed");
        }
    };

    return (
        <form className="auth-form" onSubmit={handleSubmit}>
            <h2>Register</h2>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
            <input type="text" value={role} onChange={(e) => setRole(e.target.value)} placeholder="Role" required />
            <button type="submit">Register</button>
            <p>Already have an account? <button type="button" onClick={onSwitchToLogin}>Login</button></p>
        </form>
    );
}

export default Register;