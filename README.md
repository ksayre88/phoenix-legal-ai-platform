***Please note I am not a professional programmer, I am a lawyer. A demo of this platform is available at https://api.linuxlawyer.com/ui
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

---

## 📁 Project Structure



phoenix-legal-ai-platform/
│
├── app.py # FastAPI application entrypoint
├── north_star_config.py # Global contract rules
├── persona_delta.py # Persona-based redline generator
├── redline_apply.py # DOCX tracked change generator
├── redline_docx.py # High-fidelity XML DOCX redline engine
├── semantic_matcher.py # Clause matching + embeddings
│
├── requirements.txt
├── README.md
├── LICENSE
│
└── ui/ # Front-end demo (HTML/JS/CSS)


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

## 1. **Clone the Repository**

```bash
git clone https://github.com/<your-username>/phoenix-legal-ai-platform.git
cd phoenix-legal-ai-platform

2. Create a Virtual Environment

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate


Windows PowerShell:

python -m venv .venv
.venv\Scripts\activate

3. Install Python Dependencies
pip install --upgrade pip
pip install -r requirements.txt


Dependencies include:

FastAPI

Uvicorn

httpx

chromadb

sentence-transformers

python-docx + lxml

numpy

and other standard helpers

4. Download or Install Models
For embeddings:
SentenceTransformer("all-MiniLM-L6-v2")


Downloaded automatically on first run.

For LLM inference (Ollama):

Install Ollama (if you want local LLMs):

https://ollama.ai/download

Then pull a model (example):

ollama pull llama3:instruct


Update app.py with the model name you prefer.

5. Start the Phoenix API

From the project directory:

uvicorn app:app --host 0.0.0.0 --port 8000 --reload


You should see:

INFO: 	Uvicorn running on http://0.0.0.0:8000

6. Access the Web UI

If you are using the included demo UI:

Open → ui/index.html in your browser
OR

Point your WordPress/HTML widget to:

http://localhost:8000/api/legal/query
http://localhost:8000/api/intake/analyze
http://localhost:8000/api/contracts/... etc.

🧪 Testing the API (Examples)
Statutory Query:
curl -X POST http://localhost:8000/api/legal/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Does Michigan require breach notification?", "states": ["mi","ca"]}'

Intake Request:
curl -X POST http://localhost:8000/api/intake/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "We received a customer complaint about a data breach."}'

Contract Redline Request:
curl -X POST http://localhost:8000/api/contracts/redline \
  -F "template=@template.docx" \
  -F "counterparty=@cp.docx" \
  -F "persona=General Counsel"

🛡️ Security

Phoenix:

runs entirely on your hardware

stores no data at rest

sends no data to cloud providers

is compatible with air-gapped environments

Perfect for legal teams with strict confidentiality and data residency requirements.

📜 License

Phoenix is open-source under the GPL 3.0 License.

⭐ Contributing

Pull requests are welcome!
This project is designed for legal engineers, developers, and tech-forward attorneys building internal tooling.


💬 Questions or Collaboration

For consulting, implementation help, or custom AI tooling for your legal department, feel free to reach out linuxlawyer.com or shawn@shawnclarklaw.com


