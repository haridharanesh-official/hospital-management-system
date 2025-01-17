import React, { useState } from "react";
import axios from "axios";

function App() {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState("");

    const handleQuery = async () => {
        try {
            const res = await axios.post("/ask_ai", { query });
            setResponse(res.data.response);
        } catch (error) {
            console.error("Error fetching AI response", error);
            setResponse("Error fetching response");
        }
    };

    return (
        <div className="App">
            <h1>Medical AI Assistant</h1>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask the AI..."
            />
            <button onClick={handleQuery}>Submit</button>
            <p>Response: {response}</p>
        </div>
    );
}

export default App;
