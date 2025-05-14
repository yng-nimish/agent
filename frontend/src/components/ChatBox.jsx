import React, { useState } from "react";

function ChatBox() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    const res = await fetch(
      "https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/chat",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      }
    );
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="text"
        className="w-full p-2 border rounded mb-2"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleSubmit}
      >
        Send
      </button>
      {response && <p className="mt-2">Response: {response}</p>}
    </div>
  );
}

export default ChatBox;
