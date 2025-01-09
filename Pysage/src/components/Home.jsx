import React, { useState } from 'react';

const Home = () => {
  const [prompt, setPrompt] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [displayedOutput, setDisplayedOutput] = useState('');

  const handleGenerateOutput = async () => {
    setLoading(true);
    setDisplayedOutput('');
    setOutput('');

    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: prompt }),
      });

      const data = await response.json();
      if (data.response) {
        setOutput(data.response);
        displayOutputGradually(data.response);
      } else {
        setOutput('Error generating output.');
      }
    } catch (error) {
      setOutput('Error connecting to the server.');
    } finally {
      setLoading(false);
    }
  };

  const displayOutputGradually = (text) => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplayedOutput((prev) => prev + text[index]);
      index++;
      if (index === text.length) clearInterval(interval);
    }, 50);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleGenerateOutput();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 relative">
      <div className="w-full max-w-screen-xl px-4 flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-6 text-center">Hi, I am Pysage</h1>
        <p className="text-lg mb-8 text-center">How can I help you today?</p>

        {/* Input box */}
        <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 text-center mb-5 ">
        <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full border-none rounded-lg p-4 text-lg bg-pink-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter the prompt"
          />
        </div>

        {/* Output box */}
        {loading ? (
          <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 text-center">
            <p className="text-gray-700 font-medium mb-4 text-lg">Generating output...</p>
            <div className="spinner border-t-4 border-blue-500 rounded-full w-12 h-12 mx-auto animate-spin"></div>
          </div>
        ) : (
          output && (
            <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 text-center">
              <p className="text-gray-700 font-medium mb-4 text-lg">Pysage has generated your output:</p>
              <div className="border border-gray-300 rounded-lg p-6 bg-gray-50 text-lg">
                {displayedOutput || <span className="text-gray-400">Your output will be displayed here.</span>}
              </div>
            </div>
          )
        )}
      </div>
      <p className="absolute bottom-4 right-4 text-xs text-gray-500">warning: The generated output maybe incorrect due to model inaccuracy</p>
    </div>
  );
};

export default Home;
