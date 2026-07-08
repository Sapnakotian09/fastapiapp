import { useState } from "react";
import { analyseResume } from "../Services/RagService";
import "./ResumeAnalyzer.css";

function ResumeAnalyzer() {
    const [resumeText, setResumeText] = useState("");
    const [analysis, setAnalysis] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async () => {
        if (!resumeText.trim()) {
            setError("Please paste your resume text before analyzing.");
            setAnalysis(null);
            return;
        }

        setLoading(true);
        setError(null);
        setAnalysis(null);

        try {
            const result = await analyseResume(resumeText.trim());
            setAnalysis(result.analysis);
        } catch (err: any) {
            setError(err?.response?.data?.detail || err?.message || "Unable to analyze resume.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="resume-section">
            <div className="resume-header">
                <h2>Resume Analyzer</h2>
                <p>Paste your resume content below to get analysis and improvement suggestions.</p>
            </div>
            <textarea
                className="resume-input"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume text here..."
                rows={10}
            />
            <div className="resume-actions">
                <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
                    {loading ? "Analyzing..." : "Analyze Resume"}
                </button>
            </div>
            {error && <div className="resume-error">{error}</div>}
            {analysis && (
                <div className="resume-result">
                    <h3>Analysis Result</h3>
                    <div className="resume-analysis-text">
                        {analysis.split("\n").map((line, index) => {
                            const trimmed = line.trim();
                            if (!trimmed) {
                                return <br key={index} />;
                            }
                            if (trimmed.startsWith("- ")) {
                                return <li key={index}>{trimmed.slice(2)}</li>;
                            }
                            if (trimmed.endsWith(":")) {
                                return <h4 key={index}>{trimmed}</h4>;
                            }
                            return <p key={index}>{trimmed}</p>;
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResumeAnalyzer;
