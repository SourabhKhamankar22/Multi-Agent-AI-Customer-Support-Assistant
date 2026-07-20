"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

type Message = {
  role: "user" | "assistant";
  content: string;
  agent?: string;
};

export default function Home() {
  // We now start with an empty array so we can show the Welcome Screen
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  const [userEmail, setUserEmail] = useState<string>("Loading..."); 
  const [userName, setUserName] = useState<string>("User");
  const [sessionId, setSessionId] = useState<string>("");
  
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const email = payload.sub || "Unknown Email";
      
      let name = payload.name;
      const invalidNames = ["none", "null", "nan", "undefined", "user", ""];
      if (!name || invalidNames.includes(name.toString().toLowerCase())) {
        name = email.split("@")[0];
      }

      setUserEmail(email); 
      setUserName(name);
      
      setSessionId(`session_${Date.now()}`);
    } catch (e) {
      console.error("Failed to parse token");
      localStorage.removeItem("token");
      router.push("/login");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  const startNewChat = () => {
    setSessionId(`session_${Date.now()}`);
    setMessages([]); // Clears the screen to show the suggestion cards again
  };

  const loadPastHistory = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await axios.get("http://127.0.0.1:8000/history", {
        headers: { Authorization: `Bearer ${token}` }
      });

      const historyData = response.data.history;
      if (historyData.length > 0) {
        const formattedHistory: Message[] = [];
        historyData.forEach((chat: any) => {
          formattedHistory.push({ role: "user", content: chat.user_message });
          formattedHistory.push({ 
            role: "assistant", 
            content: chat.ai_response, 
            agent: chat.agent_used 
          });
        });
        setMessages(formattedHistory);
      } else {
        alert("No past conversation history found.");
      }
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  };

  // Centralized function to handle sending messages (used by both input and suggestion cards)
  const handleSendRequest = async (text: string) => {
    if (!text.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setIsLoading(true);

    const token = localStorage.getItem("token");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat", 
        { query: text, session_id: sessionId },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.response,
          agent: response.data.agent_used,
        },
      ]);
    } catch (error) {
      console.error("Backend connection error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "🚨 Error: Cannot connect to the FastAPI backend or session expired." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendRequest(input);
  };

  return (
    <main className="flex h-screen bg-[#0B0F19] text-gray-100 font-sans overflow-hidden">
      
      {/* SIDEBAR */}
      <aside className="w-64 bg-[#111827] border-r border-gray-800 flex flex-col justify-between hidden md:flex z-10 shadow-xl">
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="p-6 pb-2">
            <h1 className="text-xl font-bold text-blue-500 tracking-wide flex items-center gap-2">
              <svg className="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              TechMart AI
            </h1>
            <p className="text-xs text-gray-500 mt-1">Multi-Agent RAG Pipeline</p>
          </div>

          <div className="px-4 mt-4">
            <button 
              onClick={startNewChat}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 px-4 rounded-xl text-sm font-medium transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-900/20"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
              New Conversation
            </button>
          </div>

          <div className="px-4 mt-6 flex-1 overflow-y-auto">
             <p className="text-xs font-semibold text-gray-500 mb-3 uppercase tracking-wider">Recent Sessions</p>
             <div className="space-y-1">
                <button 
                  onClick={loadPastHistory}
                  className="w-full text-left truncate px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-700 bg-gray-800 rounded-lg transition border border-gray-700"
                >
                  <span className="opacity-50 mr-2">🕒</span> View Past History
                </button>
             </div>
          </div>
        </div>

        <div className="p-4 pb-16 border-t border-gray-800 bg-[#0B0F19]/50">
          <div className="flex items-center justify-between px-2 pt-2">
            <div className="flex items-center gap-3 truncate">
              <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
                {userEmail !== "Loading..." ? userEmail.charAt(0).toUpperCase() : "U"}
              </div>
              <div className="truncate">
                <p className="text-sm font-medium text-gray-200 truncate max-w-[110px]" title={userName}>
                  {userName}
                </p>
                <p className="text-[10px] text-green-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span> Logged in
                </p>
              </div>
            </div>
            
            <button 
              onClick={handleLogout}
              title="Logout"
              className="text-gray-500 hover:text-red-400 p-2 rounded-lg hover:bg-gray-800 transition"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
            </button>
          </div>
        </div>
      </aside>

      {/* MAIN CHAT AREA */}
      <section className="flex-1 flex flex-col relative bg-gradient-to-b from-[#0B0F19] to-[#111827]">
        
        {/* NEW HEADER - Shows the available agents like the reference image */}
        <div className="hidden md:flex items-center justify-between p-4 border-b border-gray-800 bg-[#0B0F19]/80 backdrop-blur-sm z-10">
          <div>
            <h2 className="text-sm font-bold text-gray-200">Multi-Agent AI Customer Support</h2>
            <p className="text-xs text-green-400 flex items-center gap-1 mt-0.5">
              <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span> using RAG and LLMs (5 agents ready)
            </p>
          </div>
          
          <div className="flex flex-wrap gap-2">
             <span className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs rounded-full font-medium">⚡ Billing</span>
             <span className="px-3 py-1 bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 text-xs rounded-full font-medium">⚙️ Technical</span>
             <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-full font-medium">🛍️ Product</span>
             <span className="px-3 py-1 bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs rounded-full font-medium">📢 Complaint</span>
             <span className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs rounded-full font-medium">❓ FAQ</span>
          </div>
        </div>

        {/* Mobile Header (visible only on small screens) */}
        <div className="md:hidden flex items-center justify-between bg-[#111827] p-4 border-b border-gray-800">
          <h1 className="text-lg font-bold text-indigo-500 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            TechMart AI
          </h1>
          <button onClick={handleLogout} className="text-gray-400 text-sm hover:text-white">Logout</button>
        </div>

        {/* CHAT MESSAGES / EMPTY STATE */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-6 scroll-smooth">
          
          {/* WELCOME SCREEN - Only shows if there are no messages */}
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center max-w-3xl mx-auto text-center px-4 fade-in">
              <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-indigo-900/20">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
              </div>
              <h2 className="text-3xl font-bold text-white mb-3 tracking-tight">How can I help you today?</h2>
              <p className="text-gray-400 text-sm max-w-md mx-auto mb-10 leading-relaxed">
                I'm your Multi-Agent AI Customer Support Assistant using RAG and LLMs. Ask me anything about billing, technical support, products, or policies.
              </p>

              {/* Suggestion Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
                <button 
                  onClick={() => handleSendRequest("I was charged twice this month")}
                  className="bg-[#1F2937]/50 border border-gray-700 hover:border-indigo-500 hover:bg-[#1F2937] p-4 rounded-xl text-left transition duration-200 group"
                >
                  <div className="text-indigo-400 text-sm font-semibold mb-1 flex items-center gap-2">
                    ⚡ Billing 
                  </div>
                  <div className="text-gray-300 text-sm group-hover:text-white">I need to request a refund for my recent order</div>
                </button>
                
                <button 
                  onClick={() => handleSendRequest("My laptop won't connect to Wi-Fi")}
                  className="bg-[#1F2937]/50 border border-gray-700 hover:border-yellow-500 hover:bg-[#1F2937] p-4 rounded-xl text-left transition duration-200 group"
                >
                  <div className="text-yellow-400 text-sm font-semibold mb-1 flex items-center gap-2">
                    ⚙️ Technical 
                  </div>
                  <div className="text-gray-300 text-sm group-hover:text-white">How do I reset my account password?</div>
                </button>

                <button 
                  onClick={() => handleSendRequest("Compare Nova 15 Pro vs Nova 15")}
                  className="bg-[#1F2937]/50 border border-gray-700 hover:border-emerald-500 hover:bg-[#1F2937] p-4 rounded-xl text-left transition duration-200 group"
                >
                  <div className="text-emerald-400 text-sm font-semibold mb-1 flex items-center gap-2">
                    🛍️ Product 
                  </div>
                  <div className="text-gray-300 text-sm group-hover:text-white">Is the SmartWatch Series 8 currently in stock?</div>
                </button>

                <button 
                  onClick={() => handleSendRequest("What is your return policy?")}
                  className="bg-[#1F2937]/50 border border-gray-700 hover:border-cyan-500 hover:bg-[#1F2937] p-4 rounded-xl text-left transition duration-200 group"
                >
                  <div className="text-cyan-400 text-sm font-semibold mb-1 flex items-center gap-2">
                    ❓ FAQ 
                  </div>
                  <div className="text-gray-300 text-sm group-hover:text-white">Do you offer international shipping?</div>
                </button>
              </div>
            </div>
          )}

          {/* Active Messages List */}
          {messages.map((msg, index) => (
            <div key={index} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
              <div 
                className={`max-w-[85%] sm:max-w-[70%] p-4 rounded-2xl ${
                  msg.role === "user" 
                    ? "bg-indigo-600 text-white rounded-br-sm shadow-md" 
                    : "bg-[#1F2937] text-gray-100 rounded-bl-sm border border-gray-700 shadow-lg"
                }`}
              >
                <p className="whitespace-pre-wrap leading-relaxed text-sm sm:text-base">{msg.content}</p>
              </div>
              
              {msg.agent && (
                <span className="text-[11px] text-gray-400 mt-2 ml-1 flex items-center gap-1.5 font-medium px-2.5 py-1 bg-[#1F2937] border border-gray-700 rounded-md">
                  <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
                  Handled by {msg.agent}
                </span>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex items-start">
              <div className="bg-[#1F2937] border border-gray-700 p-4 rounded-2xl rounded-bl-sm flex items-center gap-2 shadow-lg">
                 <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></span>
                 <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce delay-75"></span>
                 <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce delay-150"></span>
              </div>
            </div>
          )}
        </div>

        {/* INPUT BOX */}
        <div className="p-4 sm:p-6 bg-transparent border-t border-gray-800">
          <form onSubmit={sendMessage} className="max-w-4xl mx-auto relative flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything — billing, technical, products, or policies..."
              className="w-full bg-[#1F2937] text-white placeholder-gray-500 border border-gray-700 rounded-xl py-4 pl-5 pr-14 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition shadow-lg text-sm sm:text-base"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="absolute right-2 bg-indigo-600 hover:bg-indigo-700 text-white p-2.5 rounded-lg transition disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
            </button>
          </form>
          <div className="text-center mt-3 hidden sm:block">
            <p className="text-[11px] text-gray-500 tracking-wide">Multi-Agent AI can make mistakes. Please verify important information.</p>
          </div>
        </div>
        
      </section>
    </main>
  );
}