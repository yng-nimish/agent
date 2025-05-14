import React, { useState } from "react";

function Recommendation() {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);

  const handleSubmit = async () => {
    const res = await fetch(
      "https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/recommend",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      }
    );
    const data = await res.json();
    setProducts(data.products);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="text"
        className="w-full p-2 border rounded mb-2"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., t-shirt for sports"
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

export default Recommendation;
