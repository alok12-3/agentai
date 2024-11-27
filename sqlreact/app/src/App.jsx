// // import React, { useState } from "react";
// // import axios from "axios";
// // import "./App.css";

// // function App() {
// //   const [csvFile, setCsvFile] = useState(null);
// //   const [query, setQuery] = useState("");
// //   const [result, setResult] = useState("");
// //   const [uploadMessage, setUploadMessage] = useState("");

// //   // Handle CSV file selection
// //   const handleFileChange = (event) => {
// //     setCsvFile(event.target.files[0]);
// //   };

// //   // Handle CSV file upload
// //   const handleFileUpload = async () => {
// //     const formData = new FormData();
// //     formData.append("file", csvFile);

// //     try {
// //       const response = await axios.post(
// //         "http://127.0.0.1:5000/upload_csv",
// //         formData,
// //         {
// //           headers: {
// //             "Content-Type": "multipart/form-data",
// //           },
// //         }
// //       );
// //       setUploadMessage(response.data.message);
// //     } catch (error) {
// //       console.error("Error uploading file:", error);
// //       setUploadMessage("File upload failed.");
// //     }
// //   };

// //   // Handle query submission
// //   const handleQuerySubmit = async () => {
// //     try {
// //       const response = await axios.post(
// //         "http://127.0.0.1:5000/execute_analysis",
// //         {
// //           query: query,
// //         }
// //       );
// //       setResult(response.data.result);
// //     } catch (error) {
// //       console.error("Error executing query:", error);
// //       setResult("Query execution failed.");
// //     }
// //   };

// //   return (
// //     <div className="App">
// //       <h1>Crew AI Data Analysis</h1>

// //       {/* CSV File Upload Section */}
// //       <div className="upload-section">
// //         <h2>Upload CSV File</h2>
// //         <input type="file" onChange={handleFileChange} />
// //         <button onClick={handleFileUpload}>Upload</button>
// //         <p>{uploadMessage}</p>
// //       </div>

// //       {/* Query Submission Section */}
// //       <div className="query-section">
// //         <h2>Submit Query</h2>
// //         <textarea
// //           placeholder="Enter your query here"
// //           value={query}
// //           onChange={(e) => setQuery(e.target.value)}
// //         ></textarea>
// //         <button onClick={handleQuerySubmit}>Submit Query</button>
// //       </div>

// //       {/* Display Result */}
// //       <div className="result-section">
// //         <h2>Query Result</h2>
// //         <pre>{result}</pre>
// //       </div>
// //     </div>
// //   );
// // }

// export default App;

import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setError(null);
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data.analysis_result); // Assuming the backend returns the analysis result
    } catch (error) {
      setError("Error uploading the file. Please try again.");
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1>CSV to SQL Conversion and Analysis</h1>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload and Analyze</button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h2>Analysis Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

// import React, { useState } from "react";
// import axios from "axios";
// import "./App.css";

// function App() {
//   const [file, setFile] = useState(null);
//   const [query, setQuery] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState(null);

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };

//   const handleQueryChange = (event) => {
//     setQuery(event.target.value);
//   };

//   const handleFileUpload = async () => {
//     if (!file || !query) {
//       setError("Please select a file and enter a query.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append("query", query);

//     try {
//       setError(null);
//       const response = await axios.post(
//         "http://localhost:5000/upload",
//         formData,
//         {
//           headers: {
//             "Content-Type": "multipart/form-data",
//           },
//         }
//       );

//       setResult(response.data.analysis_result);
//     } catch (error) {
//       setError("Error uploading the file. Please try again.");
//       console.error(error);
//     }
//   };

//   return (
//     <div className="App">
//       <h1>CSV to SQL Conversion and Analysis</h1>
//       <input type="file" accept=".csv" onChange={handleFileChange} />
//       <input
//         type="text"
//         placeholder="Enter your query"
//         value={query}
//         onChange={handleQueryChange}
//       />
//       <button onClick={handleFileUpload}>Upload and Analyze</button>

//       {error && <div className="error">{error}</div>}

//       {result && (
//         <div className="result">
//           <h2>Analysis Result</h2>
//           <pre>{JSON.stringify(result, null, 2)}</pre>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;
