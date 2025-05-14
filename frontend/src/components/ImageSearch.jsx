import React, { useState } from "react";

function ImageSearch() {
  const [file, setFile] = useState(null);
  const [products, setProducts] = useState([]);

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("image", file);
    const res = await fetch(
      "https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/image-search",
      {
        method: "POST",
        body: formData,
      }
    );
    const data = await res.json();
    setProducts(data.products);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="file"
        accept="image/*"
        className="mb-2"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleSubmit}
      >
        Search
      </button>
      <div className="mt-4">
        {products.map((product) => (
          <div key={product.id} className="border p-2 mb-2">
            <p>{product.name}</p>
            <p>${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ImageSearch;
