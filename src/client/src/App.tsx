import { useState } from "react";
import { FaSearch } from "react-icons/fa";

interface CheckResult {
  similarity: number;
  plagiarism_level: string;
  test_file: string;
  reference_file: string;
}

function App(): JSX.Element {
  const [referenceFile, setReferenceFile] = useState<File | null>(null);
  const [testFile, setTestFile] = useState<File | null>(null);
  const [checkResult, setCheckResult] = useState<CheckResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [showAlert, setShowAlert] = useState<boolean>(false);

  const handleReferenceUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://localhost:5000/upload/reference", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          setReferenceFile(file);
          setCheckResult(null);
          setShowAlert(false);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleTestUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://localhost:5000/upload/test", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          setTestFile(file);
          setCheckResult(null);
          setShowAlert(false);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleCheck = async (): Promise<void> => {
    if (!referenceFile || !testFile) {
      setShowAlert(true);
      setTimeout(() => setShowAlert(false), 3000);
      return;
    }

    setLoading(true);
    setShowAlert(false);
    try {
      const response = await fetch("http://localhost:5000/check");
      const data: CheckResult = await response.json();
      setCheckResult(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Error checking plagiarism");
    }
    setLoading(false);
  };

  const formatSimilarity = (similarity: number): string => {
    return (similarity * 100).toFixed(2) + "%";
  };

  const getPlagiarismColor = (plagiarismLevel: string): string => {
    switch (plagiarismLevel) {
      case "Plagiarisme Berat":
        return "text-red-600";
      case "Plagiarisme Sedang":
        return "text-orange-500";
      case "Plagiarisme Ringan":
        return "text-yellow-600";
      case "Tidak Plagiarisme":
        return "text-green-600";
      default:
        return "text-gray-600";
    }
  };

  return (
    <div className="min-h-screen bg-yellow-500 text-black flex flex-col items-center py-10">
      {showAlert && (
        <div className="fixed bottom-12 right-12 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-lg slide-up-alert">
          Please upload both reference and test files before checking for
          plagiarism.
        </div>
      )}

      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-zinc-900">Plagiarism Checker</h1>
        <p className="mt-6 text-2xl text-white bg-red-600 py-3 px-6 rounded-lg font-semibold">
          Detect Plagiarism, Preserve Originality
        </p>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 mt-10">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Reference Document */}
          <div className="bg-yellow-100 border border-zinc-900 rounded-lg p-6 flex-1 shadow-lg transition-all duration-300 hover:shadow-2xl">
            <h2 className="text-2xl font-semibold mb-4 text-zinc-900">
              Reference Document
            </h2>
            <p className="text-zinc-700 mb-6">
              {referenceFile
                ? referenceFile.name
                : "Upload the document you want to use as a reference for comparison."}
            </p>
            <label
              htmlFor="referenceUpload"
              className="font-bold block w-full p-4 text-center text-yellow-500 bg-zinc-900 hover:bg-zinc-800 rounded-lg cursor-pointer transition duration-300"
            >
              Upload Reference PDF
            </label>
            <input
              type="file"
              id="referenceUpload"
              accept=".pdf"
              className="hidden"
              onChange={handleReferenceUpload}
            />
          </div>

          {/* Test Document */}
          <div className="bg-yellow-100 border border-zinc-900 rounded-lg p-6 flex-1 shadow-lg transition-all duration-300 hover:shadow-2xl">
            <h2 className="text-2xl font-semibold mb-4 text-zinc-900">
              Test Document
            </h2>
            <p className="text-zinc-700 mb-6">
              {testFile
                ? testFile.name
                : "Upload the document you want to check for plagiarism."}
            </p>
            <label
              htmlFor="testUpload"
              className="font-bold block w-full p-4 text-center text-yellow-500 bg-zinc-900 hover:bg-zinc-800 rounded-lg cursor-pointer transition duration-300"
            >
              Upload Test PDF
            </label>
            <input
              type="file"
              id="testUpload"
              accept=".pdf"
              className="hidden"
              onChange={handleTestUpload}
            />
          </div>
        </div>

        {/* Check Button */}
        <div className="mt-8 flex justify-center">
          <button
            className="flex items-center space-x-3 px-6 py-3 text-white font-semibold bg-zinc-900 hover:bg-zinc-800 rounded-lg shadow-lg transition duration-300 transform hover:scale-105"
            onClick={handleCheck}
            disabled={loading}
          >
            <FaSearch />
            <span>{loading ? "Checking..." : "Check!"}</span>
          </button>
        </div>

        {/* Results Section */}
        {checkResult && (
          <div className="mt-8">
            <div className="bg-white rounded-lg p-6 shadow-lg max-w-2xl mx-auto">
              <h3 className="text-xl font-semibold mb-4 text-zinc-900">
                Plagiarism Check Results
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Similarity Score:</span>
                  <span
                    className={`font-bold ${getPlagiarismColor(
                      checkResult.plagiarism_level
                    )}`}
                  >
                    {formatSimilarity(checkResult.similarity)}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Plagiarism Level:</span>
                  <span
                    className={`font-bold ${getPlagiarismColor(
                      checkResult.plagiarism_level
                    )}`}
                  >
                    {checkResult.plagiarism_level}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Test File:</span>
                  <span className="text-gray-600">{checkResult.test_file}</span>
                </div>
                <div className="flex justify-between items-center pb-2">
                  <span className="font-medium">Reference File:</span>
                  <span className="text-gray-600">
                    {checkResult.reference_file}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
