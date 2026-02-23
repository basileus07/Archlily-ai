# 🧠 ArchLily Development Plan

## 🎯 Goal

Build a production-grade **AI System Design Interview Agent** using:

- **FastAPI**
- **PostgreSQL**
- **OpenAI**
- **React**

---

## 🚀 Phase 1 — Foundation

**Objective:** Build minimal working backend with database + OpenAI integration.

**Tasks:**

- Setup project structure
- Setup virtual environment
- Install dependencies
- Run PostgreSQL via Docker
- Connect FastAPI to PostgreSQL
- Create basic models:
  - User
  - Session
  - Message
- Create `/chat` endpoint
- Call OpenAI API
- Save user message + AI response to database
- Return response

**Result:**

- → Backend works  
- → Data persists  
- → AI responds  

---

## 🚀 Phase 2 — Conversation Memory

**Objective:** Make ArchLily remember conversation context.

**Tasks:**

- Fetch previous messages from DB
- Send history to OpenAI
- Maintain conversation thread
- Optional: Add streaming

**Result:**

- → Context-aware agent  

---

## 🚀 Phase 3 — RAG (Knowledge System)

**Objective:** Allow ArchLily to use system design documents.

**Tasks:**

- Setup vector database (FAISS / Pinecone)
- Add embedding pipeline
- Store system design templates
- Retrieve relevant chunks before answering
- Inject into prompt

**Result:**

- → Intelligent domain-aware agent  

---

## 🚀 Phase 4 — Tool Calling

**Objective:** Allow ArchLily to take actions.

**Possible tools:**

- Cost estimator
- Traffic calculator
- Diagram generator
- Database recommender

**Result:**

- → Agent can reason + act  

---

## 🚀 Phase 5 — ReAct Pattern

**Objective:** Implement reasoning loop.

1. Think  
2. Choose tool  
3. Observe  
4. Think again  
5. Final answer  

**Result:**

- → Autonomous behavior  

---

## 🚀 Phase 6 — Evaluator Pattern

**Objective:** Score and improve system design answers.

- Critic agent
- Feedback loop
- Optimization

**Result:**

- → Self-improving agent  

---

## 🚀 Phase 7 — Multi-Agent Orchestration

**Agents:**

- Requirement Clarifier
- HLD Designer
- Deep Dive Engineer
- Critic

**Result:**

- → Distributed AI architecture  

---

## 🚀 Phase 8 — MCP Integration

- External tool servers
- Semantic tool discovery
- Plug-and-play architecture

**Result:**

- → Enterprise-ready AI system  

## cmd
- uvicorn app.main:app --reload
- docker exec -it archlily-db psql -U archlily -d archlily (verify in database) SELECT * FROM messages; (/q /? /;)









