import React, { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import ImageUpload from "./components/ImageUpload";
import "./index.css";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-4">Commerce AI Agent</h1>
      <div className="tabs mb-4">
        <button
          className={`px-4 py-2 ${
            activeTab === "chat" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
          onClick={() => setActiveTab("chat")}
        >
          Chat
        </button>
        <button
          className={`px-4 py-2 ${
            activeTab === "image" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
          onClick={() => setActiveTab("image")}
        >
          Image Search
        </button>
      </div>
      <div className="w-full max-w-2xl">
        {activeTab === "chat" ? <ChatInterface /> : <ImageUpload />}
      </div>
    </div>
  );
}

export default App;
