A demo of this platform is available at https://api.linuxlawyer.com/ui
This repository does not include the RAG or dataset for Michigan and California statutes.

# Phoenix: Internally-Hosted Legal AI Platform

Phoenix is a fully self-hosted legal AI platform designed for modern in-house legal teams.  
It provides:

- **Multi-state statutory research** using Retrieval-Augmented Generation (RAG)
- **Automated legal intake classification, routing, and prioritization**
- **Contract clause comparison, semantic matching, and persona-driven redlines**
- **DOCX redline export with tracked changes and analysis reports**

Phoenix runs entirely on **local GPU hardware**, uses **open-source models**, and supports full customization of legal workflows — without vendor lock-in, cloud dependencies, or data leaving your environment.

---

## 🔧 Features

### **Statutory Research**
- Michigan + California statutes included in demo  
- Multi-state queries  
- Citation-first persona responses  
- Multi-pass RAG retrieval (up to 60 chunks)  
- 1–3 second response time on modest GPU hardware  

### **Intake Engine**
- Automatic category classification  
- Priority scoring (rubric-based)  
- C-suite name detection  
- Summaries + suggested next steps  
- Skill-weighted team routing  
- JSON-mode for stable downstream use  

### **Contract Engine**
- Semantic clause matching (MiniLM embeddings)  
- Persona-based redlines (GC, Deal Maker, Litigator, custom personas)  
- Global “North Star” contract rules  
- Section-specific rules (Indemnification, Liability, Termination, Confidentiality)  
- Structured deltas (insert/delete/replace/comments)  
- DOCX redline export (tracked changes + comments)  

### **Policy Mapper**
- Upload policies (DOCX/PDF/HTML/TXT) for structured summaries  
- Extracts standardized data types for downstream analysis  
- JSON-ready output for integrations  

### **IP Guard**
- Automatic request tracking and blocklist enforcement  
- Local admin UI for managing blocked IPs  
- Persisted blocklist on disk for reloads  

---

## 📁 Project Structure

All Python files are kept at the same level to preserve import paths and simplify installation.

---

# 🚀 Installation Guide

Phoenix requires:

- **Python 3.10+**
- **pip**
- **A GPU with CUDA support (recommended, but CPU works for testing)**
- **Ubuntu / WSL2 / macOS / Windows** (any OS supported by FastAPI + Python)

Below is a standard installation workflow.

---

1. **Clone the Repository**

```bash
git clone https://github.com/<your-username>/phoenix-legal-ai-platform.git
cd phoenix-legal-ai-platform
```

**2. Create a Virtual Environment**

Linux/macOS:
```
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:
```
python -m venv .venv
.venv\Scripts\activate
```
**3. Install Python Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Optional dependency notes:
- `chromadb` is used for the RAG statute index.
- `pypdf` is required for PDF uploads in the mapper/contract tools.

**4. Configure Environment (Optional)**
Set these as needed:
- `PHOENIX_MODEL_NAME` (default: `qwen2.5:14b`)
- `OLLAMA_URL` (default: `http://localhost:11434`)
- `CORPUS_ROOT` (default: `~/legal-rag`)
- `USE_RAG_BACKEND` (default: `True`)
- `IP_BLOCKLIST_PATH` (default: `./ip_blocklist.json`)
- `ADMIN_TOKEN` (enables `/admin/ips` IP admin UI)

**5. Download or Install Models**
For embeddings:
SentenceTransformer("all-MiniLM-L6-v2") should be downloaded automatically on first run.

For LLM inference (Ollama):

  Install Ollama (if you want local LLMs): https://ollama.ai/download

Update `main.py` or set `PHOENIX_MODEL_NAME` with the model you prefer.

**6. Start the Phoenix API**

From the project directory:

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:

INFO: 	Uvicorn running on http://0.0.0.0:8000

**7. Access the Web UI**

Open → http://127.0.0.1:8000/

📜 License

Phoenix is open-source under the GPL 3.0 License.


⭐ Contributing

Pull requests are welcome!
This project is designed for legal engineers, developers, and tech-forward attorneys building internal tooling.


💬 Questions or Collaboration

For consulting, implementation help, or custom AI tooling for your legal department, feel free to reach out at shawn@shawnclarklaw.com

