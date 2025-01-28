import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to the Flask server

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    // Listen for responses from the server
    socket.on("response", (data) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "bot", text: data.response },
      ]);
    });

    socket.on("error", (data) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "error", text: data.error },
      ]);
    });

    return () => {
      socket.off("response");
      socket.off("error");
    };
  }, []);

  const handleSend = () => {
    if (input.trim() !== "") {
      // Send user message to the server
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "user", text: input },
      ]);
      socket.emit("message", { input });
      setInput(""); // Clear the input field
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="flex flex-col h-[500px] w-[400px] border border-gray-300 rounded-lg overflow-hidden bg-white shadow-lg">
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-3 px-4 py-2 rounded-lg max-w-[80%] ${
                msg.type === "user"
                  ? "self-end bg-blue-500 text-white"
                  : msg.type === "bot"
                  ? "self-start bg-gray-200 text-black"
                  : "self-start bg-red-100 text-red-700"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className="flex items-center border-t border-gray-300 p-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={handleSend}
            className="ml-3 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
