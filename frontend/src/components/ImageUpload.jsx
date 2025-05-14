import React, { useState } from "react";
import axios from "axios";

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("image", file);

    try {
      // Update to API Gateway URL in production
      const response = await axios.post(
        "https://<api-id>.execute-api.<region>.amazonaws.com/dev/image-search",
        formData
      );
      setResults(response.data.products);
    } catch (error) {
      setResults([{ name: "Error", description: "Could not process image." }]);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="p-2 bg-blue-500 text-white rounded"
      >
        Search Products
      </button>
      <div className="mt-4">
        {results.map((product, index) => (
          <div key={index} className="p-2 border-b">
            <h3 className="font-bold">{product.name}</h3>
            <p>{product.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ImageUpload;
