import { useState } from "react";
import { FaSearch } from "react-icons/fa";

function App() {
  const [referenceFile, setReferenceFile] = useState<File | null>(null);
  const [testFile, setTestFile] = useState<File | null>(null);

  const handleReferenceUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files ? e.target.files[0] : null;
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
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleTestUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files ? e.target.files[0] : null;
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
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleCheck = async () => {
    if (!referenceFile || !testFile) {
      alert("Please upload both files first");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/check");
      const data = await response.json();
      // Handle similarity check response
      console.log(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="min-h-screen bg-yellow-500 text-black flex flex-col items-center py-10">
      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-zinc-900">Plagiarism Checker</h1>
        <p className="mt-6 text-lg text--900">
          Alert! Plagiarism Check – Keep It Clean, Keep It Yours!
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
          >
            <FaSearch />
            <p>Check!</p>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
