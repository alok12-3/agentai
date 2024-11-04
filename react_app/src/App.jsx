import React, { useState } from "react";
import "./App.css";

function App() {
  const [company, setCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showDownloadButton, setShowDownloadButton] = useState(false);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await generateReport(company);
  };

  const generateReport = async (companyName) => {
    setLoading(true);
    setError(null);
    setShowDownloadButton(false);
    setDownloadLink(null);

    try {
      const response = await fetch(
        "https://agentai-1.onrender.com/generate_report",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ company: companyName }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate report");
      }

      // Create a blob from the PDF response
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadLink(url);

      // Show the download button
      setShowDownloadButton(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Market Research & Use Case Generation Agent</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="Enter company name"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Run Research and Generate Report"}
        </button>
      </form>

      {loading && <p>This may take up to 5 minutes. Please wait patiently.</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {showDownloadButton && downloadLink && (
        <a href={downloadLink} download={`${company}_report.pdf`}>
          <button>Download Report</button>
        </a>
      )}
    </div>
  );
}

export default App;
