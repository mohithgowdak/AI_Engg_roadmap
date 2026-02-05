# Quick Start Guide - 8 Days to LangChain Mastery

Welcome! This guide will help you master LangChain in 8 days.

## 🚀 Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get an API Key

1. Sign up at [OpenAI](https://platform.openai.com/) to get an API key
2. Create a `.env` file in the root directory
3. Add your API key:

```
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Verify Setup

```bash
cd 01_Basics
python 01_basic_llm.py
```

You should see output showing how to use LangChain with an LLM!

## 📅 8-Day Learning Schedule

### **Day 1: Basics - LLMs & Prompts** (3-4 hours)
**Location**: `01_Basics/`

- **Morning (2 hours)**:
  - Run `01_basic_llm.py` - Understand LLMs
  - Experiment with different models and temperatures
  
- **Afternoon (2 hours)**:
  - Run `02_prompts.py` - Master prompts
  - Create your own prompt templates

**Goal**: Understand how to interact with LLMs using LangChain

---

### **Day 2: Basics - Chains & Parsers** (3-4 hours)
**Location**: `01_Basics/`

- **Morning (2 hours)**:
  - Run `03_chains.py` - Build chains
  - Create sequential chains
  
- **Afternoon (2 hours)**:
  - Run `04_output_parsers.py` - Parse outputs
  - Build a simple application using chains

**Goal**: Build your first LangChain application

---

### **Day 3: Memory & Conversations** (3-4 hours)
**Location**: `02_Memory_Conversations/`

- **Morning (2 hours)**:
  - Run `05_memory_basic.py` - Understand memory types
  
- **Afternoon (2 hours)**:
  - Run `06_conversation_chains.py` - Build chatbots
  - Create your first chatbot

**Goal**: Build a conversational AI with memory

---

### **Day 4: Document Processing** (3-4 hours)
**Location**: `03_Document_Processing/`

- **Morning (1.5 hours)**:
  - Run `07_document_loaders.py` - Load documents
  
- **Afternoon (2.5 hours)**:
  - Run `08_text_splitters.py` - Split text
  - Run `09_embeddings.py` - Understand embeddings
  - Process your own documents

**Goal**: Process and understand documents

---

### **Day 5: Vector Stores & RAG** (4-5 hours)
**Location**: `04_Vector_Stores_RAG/`

- **Morning (2 hours)**:
  - Run `10_vector_stores.py` - Work with vector stores
  
- **Afternoon (3 hours)**:
  - Run `11_retrieval_qa.py` - Build RAG system
  - Create a document Q&A system

**Goal**: Build your first RAG application

---

### **Day 6: Agents - Basics & Tools** (4-5 hours)
**Location**: `05_Agents/`

- **Morning (2 hours)**:
  - Run `12_agents_basic.py` - Introduction to agents
  
- **Afternoon (3 hours)**:
  - Run `13_agent_tools.py` - Create custom tools
  - Build an agent with your own tools

**Goal**: Build an intelligent agent

---

### **Day 7: Agents & Advanced Topics** (4-5 hours)
**Location**: `05_Agents/` and `06_Advanced_Topics/`

- **Morning (2 hours)**:
  - Run `14_agent_executor.py` - Advanced agents
  
- **Afternoon (3 hours)**:
  - Run `15_streaming.py` - Streaming responses
  - Run `16_callbacks.py` - Use callbacks

**Goal**: Master advanced agent features

---

### **Day 8: Advanced & Final Project** (5-6 hours)
**Location**: `06_Advanced_Topics/` and `07_Final_Project/`

- **Morning (2 hours)**:
  - Run `17_custom_chains.py` - Custom chains
  
- **Afternoon (1 hour)**:
  - Review all modules
  - Plan your project
  
- **Evening (2-3 hours)**:
  - Start building your final project
  - See `07_Final_Project/README.md` for ideas

**Goal**: Complete a LangChain project

## 📂 Folder Structure

```
Langchain/
├── 01_Basics/              # Days 1-2
├── 02_Memory_Conversations/ # Day 3
├── 03_Document_Processing/ # Day 4
├── 04_Vector_Stores_RAG/    # Day 5
├── 05_Agents/              # Days 6-7
├── 06_Advanced_Topics/     # Day 7-8
└── 07_Final_Project/       # Day 8
```

## 💡 Daily Tips

1. **Read the README** in each module folder first
2. **Run examples** to see them in action
3. **Modify code** to experiment
4. **Take notes** on key concepts
5. **Build small projects** after each day

## 🆘 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created a `.env` file in the root directory
- Check that the key starts with `sk-`

### Import errors
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8+

### Module not found errors
- Make sure you're running from the correct directory
- Use: `python 01_Basics/01_basic_llm.py` from root
- Or: `cd 01_Basics` then `python 01_basic_llm.py`

### API errors
- Check your API key is valid
- Ensure you have credits in your OpenAI account
- Check your internet connection

## 📊 Progress Checklist

Track your daily progress:

- [ ] Day 1: Basics - LLMs & Prompts ✅
- [ ] Day 2: Basics - Chains & Parsers
- [ ] Day 3: Memory & Conversations
- [ ] Day 4: Document Processing
- [ ] Day 5: Vector Stores & RAG
- [ ] Day 6: Agents - Basics & Tools
- [ ] Day 7: Agents & Advanced Topics
- [ ] Day 8: Advanced & Final Project

## 🎯 Final Project Ideas

After Day 8, build one of these:

1. **Document Q&A System** - Ask questions about your documents
2. **Intelligent Chatbot** - Chatbot with memory and tools
3. **Research Assistant** - Agent that searches and summarizes
4. **Code Explainer** - Upload code, get explanations
5. **Your Own Idea!** - Be creative!

## 🎓 Next Steps After 8 Days

1. Build more complex projects
2. Explore LangChain integrations
3. Deploy your applications
4. Contribute to open source
5. Share your projects!

Good luck! You've got this! 🚀
