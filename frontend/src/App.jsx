import React, { useState } from "react";
import ChatBox from "./components/ChatBox";
import Recommendation from "./components/Recommendation";
import ImageSearch from "./components/ImageSearch";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-6">Free AI Commerce Agent</h1>
      <div className="w-full max-w-2xl">
        <div className="flex mb-4">
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
              activeTab === "recommend"
                ? "bg-blue-500 text-white"
                : "bg-gray-200"
            }`}
            onClick={() => setActiveTab("recommend")}
          >
            Recommend
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
        {activeTab === "chat" && <ChatBox />}
        {activeTab === "recommend" && <Recommendation />}
        {activeTab === "image" && <ImageSearch />}
      </div>
    </div>
  );
}

export default App;
