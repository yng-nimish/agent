import React, { useState } from "react";
import axios from "axios";

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: "user", text: input };
    setMessages([...messages, userMessage]);
    setInput("");

    try {
      // Update to API Gateway URL in production
      const response = await axios.post(
        "https://<api-id>.execute-api.<region>.amazonaws.com/dev/chat",
        { message: input }
      );
      setMessages([
        ...messages,
        userMessage,
        { role: "agent", text: response.data.response },
      ]);
    } catch (error) {
      setMessages([
        ...messages,
        userMessage,
        { role: "agent", text: "Error: Could not connect to the server." },
      ]);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <div className="h-96 overflow-y-auto mb-4 p-2 border">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-2 ${
              msg.role === "user" ? "text-right" : "text-left"
            }`}
          >
            <span
              className={`inline-block p-2 rounded ${
                msg.role === "user" ? "bg-blue-100" : "bg-gray-100"
              }`}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-2 border rounded-l"
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="p-2 bg-blue-500 text-white rounded-r"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;
