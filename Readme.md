# Multi-Agent AI Customer Support Assistant using RAG and LLMs

An industry-level, production-ready capstone project demonstrating modern AI orchestration, semantic search, and secure multi-tier full-stack development. This system shifts away from monolithic chatbots by employing an intelligent routing mesh that delegating tasks to domains-specific AI agents equipped with Retrieval-Augmented Generation (RAG).

## 🚀 Live Deployment Links

* **Frontend Dashboard (Vercel):** [https://multi-agent-ai-customer-support-ass-iota.vercel.app](https://www.google.com/search?q=https://multi-agent-ai-customer-support-ass-iota.vercel.app)
* **Backend API Gateway (Render):** [https://multi-agent-ai-customer-support-assistant-v0fy.onrender.com](https://multi-agent-ai-customer-support-assistant-v0fy.onrender.com)
* **Database Cloud Cluster:** MongoDB Atlas Distributed Cluster

---

## 🏗️ System Architecture & Workflow

```text
                     Customer
                         │
                         ▼
                 Web Chat Interface (Next.js)
                         │
                         ▼
             Backend API Server (FastAPI Router)
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Intent Detection         Conversation Memory (MongoDB Atlas)
             │
             ▼
        Agent Router (Gemini-3.1-Flash-Lite Orchestrator)
             │
 ┌───────────┼─────────────┬──────────────┬──────────────┐
 ▼           ▼             ▼              ▼              ▼
Billing   Technical     Product       Complaint       FAQ
Agent     Agent         Agent         Agent           Agent
             │             │                             │
             └─────────────┼─────────────────────────────┘
                           ▼
                  Retrieval System (RAG)
                           │
                           ▼
                 Vector Database (FAISS Index)
                           │
                           ▼
                 Company Knowledge Base (PDFs)
                           │
                           ▼
                 Final Synthesized Response
```

### 🔁 Execution Pipeline

1. **User Authentication:** Secure ingress validation via JSON Web Tokens (JWT)[cite: 5, 6].
2. **Intent Analysis:** The Intent Orchestrator utilizes low-temperature structural schema enforcement via Pydantic to cleanly classify requests into domain boundaries[cite: 11, 12].
3. **Context Augmentation (RAG):** When specialized agents (Product/FAQ) receive requests, they generate queries to execute an asynchronous semantic similarity check against the FAISS vector database to retrieve highly accurate operational details.

4. **Generative Response Synthesis:** The system feeds the source metrics alongside the prompt data to `gemini-3.1-flash-lite` to compile cohesive, context-grounded outputs.

5. **State Persistence:** Every interaction is written dynamically to MongoDB database clusters to establish persistent long-term conversation storage[cite: 2, 12].

---

## 🛠️ Technology Stack & Software Ecosystem

### Frontend

* **Core Architecture:** Next.js (App Router) & React.js[cite: 1, 12]
* **Styling Paradigm:** Tailwind CSS (Responsive Dark Mode UI theme)[cite: 1, 12]
* **Data Ingress Clients:** Axios HTTP Engine client[cite: 1, 12]

### Backend & AI Pipelines

* **Application Engine:** Python FastAPI with strict CORS Middlewares[cite: 2, 12]
* **Orchestration Engine:** Google Gemini SDK (`gemini-3.1-flash-lite`)[cite: 3, 12]
* **RAG Processing:** LangChain Ecosystem Components (`langchain-huggingface`, `langchain-community`)[cite: 8, 9, 12]
* **Vector Engine:** FAISS Local Serialization Matrix Store[cite: 8, 9, 12]
* **Embedding Model:** Hugging Face `sentence-transformers/all-MiniLM-L6-v2`[cite: 8, 9, 12]

### Database & Storage Tier

* **Primary DB Cluster:** MongoDB Atlas Cloud Storage Node

* **Driver Layer:** Motor Asynchronous MongoDB AsyncIOMotorClient
* **Security Context:** JWT (PyJWT Engine) & Blowfish Password Hashing (`bcrypt`)[cite: 5, 6]

---

## 📂 Verified Folder Structure

```text
customer-support-ai/
│
├── backend/
│   ├── agents/
│   │     ├── billing.py      # Specialized Agent: Invoices, Subscriptions & Refunds
│   │     ├── complaint.py    # Specialized Agent: Customer Dissatisfaction & Escalation
│   │     ├── faq.py          # RAG-Augmented Agent: General Policy Retrieval
│   │     ├── product.py      # RAG-Augmented Agent: Product Specs & Catalog Metrics
│   │     ├── router.py       # Pydantic Structural Intent Detection Orchestrator
│   │     └── technical.py    # Specialized Agent: System Anomalies & Login Inquiries
│   ├── api/
│   │     └── auth.py         # Registration, Cryptographic Verification & Token Flow
│   ├── database/
│   │     └── mongodb.py      # Async Engine Configuration for MongoDB Atlas
│   ├── models/
│   │     └── user.py         # Pydantic Request Validation Schemas
│   ├── rag/
│   │     ├── ingest.py       # PDF Text Extractor & FAISS Pipeline Database Builder
│   │     └── retriever.py    # Semantic Context Ingestion Controller
│   ├── vectorstore/
│   │     └── faiss_index/    # Vector Database Binary Partitions
│   └── main.py               # Core Microservice Orchestrator
│
├── frontend/
│   ├── public/               # Static System Media Assets
│   └── src/app/
│           ├── login/        # Token Exchange View Ingress Controller
│           │   └── page.tsx
│           ├── register/     # Identity Onboarding View Panel
│           │   └── page.tsx          
│           ├── globals.css     # Tailwind Style Implementations
│           ├── layout.tsx      # System View Master Canvas
│           └── page.tsx        # High-Fidelity Asynchronous Conversational Interface
│
├── knowledge_base/           # RAG Document Corpus
│     ├── FAQ.pdf
│     ├── Pricing.pdf
│     ├── RefundPolicy.pdf
│     ├── ShippingPolicy.pdf
│     ├── UserManual.pdf
│     └── Warranty.pdf
│
├── datasets/                 # Core Evaluation Datasets Repository
├── get_data.py
├── .gitignore                # Node Cache & Virtual Env Exclusion Strategy Rules
└── requirements.txt          # Python Microservice Dependencies Manifesto
```

---

## ⚙️ Local Installation & Setup Instructions

### Prerequisites

* Python 3.11+

* Node.js 20+

* MongoDB Atlas Live Instance URI

### 1. Repository Setup & Virtual Environment

```bash
# Clone the repository
git clone https://github.com/SourabhKhamankar22/Multi-Agent-AI-Customer-Support-Assistant
cd Multi-Agent-AI-Customer-Support-Assistant-

# Initialize and launch the Python Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 2. Backend Pipeline Configuration

Create an `.env` file within the master project root path:

```env
MONGODB_URL=your_mongodb_atlas_connection_string
DATABASE_NAME=customer_support_db
GEMINI_API_KEY=your_google_gemini_api_key
JWT_SECRET=your_cryptographic_secret_hash_string
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Install standard backend execution dependencies and build the vector base:

```bash
# Install core modules
pip install -r requirements.txt

# Execute vector ingestion pipeline (Run from root dir)
python -m backend.rag.ingest

# Launch the Uvicorn Asynchronous Server Agent
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend Dashboard Application Build

Navigate into the `frontend` subfolder and start the client application development container node:

```bash
cd frontend

# Install Node modules
npm install

# Boot development container runtime engine
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the application.

---

## 📊 Application Dashboard Outputs & Deployment Evidence

### User Authentication Architecture

*Secure, structured JWT-driven user registration and login portals ensuring encrypted isolation for tenant conversational data stores.*

| User Identity Generation (`/register`) | Identity Authorization Window (`/login`) |
| --- | --- |
| ![](assets/register.png) | ![](assets/login.png) 

### High-Fidelity Multi-Agent Chat Environment

*The real-time operational dashboard executing automatic intent analysis routing across Billing, Technical, Product, Complaints, and FAQ agents.*
![Chat Environment Dashboard](assets/chat.png)

### Cloud Deployment Topologies

*Verification of fully integrated live deployment configurations operating across Render API pipelines and Vercel edge delivery networks.*

| Vercel Frontend Server Deploy Pipeline | Render Application Engine logs Cluster |
| --- | --- |
|  |  |

---

## 🎓 Evaluation & Implementation Matrix Met

* **Frontend Design:** Completed customized modern dark mode workspace featuring isolated multi-agent tracking chips and continuous conversation persistence[cite: 1, 12].
* **Backend REST Layer:** Implemented asynchronous endpoints built on FastAPI featuring strict cryptographically salted validation mechanics[cite: 2, 5, 6, 12].
* **Multi-Agent Router Systems:** Intent detection routing engine powered by `gemini-3.1-flash-lite` utilizing structural JSON responses generated via Pydantic model configurations[cite: 11, 12].
* **RAG System Architectures:** Local index retrieval pipeline powered by a FAISS engine utilizing localized structural serialization strategies[cite: 8, 9, 12].
* **Database Architectures:** Fully implemented production database topology scaling dynamically via MongoDB Atlas.