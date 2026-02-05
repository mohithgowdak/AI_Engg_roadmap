# LangChain Learning Path - From Scratch

Welcome to your comprehensive LangChain learning journey! This repository contains structured examples organized by modules to help you master LangChain step by step.

## 📁 Repository Structure

```
Langchain/
├── 01_Basics/                    # Module 1: Core Concepts
│   ├── 01_basic_llm.py
│   ├── 02_prompts.py
│   ├── 03_chains.py
│   ├── 04_output_parsers.py
│   └── README.md
├── 02_Memory_Conversations/      # Module 2: Chatbots & Memory
│   ├── 05_memory_basic.py
│   ├── 06_conversation_chains.py
│   └── README.md
├── 03_Document_Processing/      # Module 3: Document Handling
│   ├── 07_document_loaders.py
│   ├── 08_text_splitters.py
│   ├── 09_embeddings.py
│   └── README.md
├── 04_Vector_Stores_RAG/         # Module 4: RAG Systems
│   ├── 10_vector_stores.py
│   ├── 11_retrieval_qa.py
│   └── README.md
├── 05_Agents/                    # Module 5: Intelligent Agents
│   ├── 12_agents_basic.py
│   ├── 13_agent_tools.py
│   ├── 14_agent_executor.py
│   └── README.md
├── 06_Advanced_Topics/           # Module 6: Advanced Features
│   ├── 15_streaming.py
│   ├── 16_callbacks.py
│   ├── 17_custom_chains.py
│   └── README.md
├── 07_Final_Project/            # Your Project Here!
│   └── README.md
├── requirements.txt
├── QUICK_START.md
└── README.md (this file)
```

## 📅 8-Day Learning Plan

### **Day 1: Basics - LLMs & Prompts**
- **Morning**: `01_Basics/01_basic_llm.py` - Learn about LLMs
- **Afternoon**: `01_Basics/02_prompts.py` - Master prompts and templates
- **Evening**: Practice creating your own prompts

### **Day 2: Basics - Chains & Parsers**
- **Morning**: `01_Basics/03_chains.py` - Build chains
- **Afternoon**: `01_Basics/04_output_parsers.py` - Parse outputs
- **Evening**: Build a simple chain application

### **Day 3: Memory & Conversations**
- **Morning**: `02_Memory_Conversations/05_memory_basic.py` - Understand memory
- **Afternoon**: `02_Memory_Conversations/06_conversation_chains.py` - Build chatbots
- **Evening**: Create your first chatbot

### **Day 4: Document Processing**
- **Morning**: `03_Document_Processing/07_document_loaders.py` - Load documents
- **Afternoon**: `03_Document_Processing/08_text_splitters.py` - Split text
- **Evening**: `03_Document_Processing/09_embeddings.py` - Understand embeddings

### **Day 5: Vector Stores & RAG**
- **Morning**: `04_Vector_Stores_RAG/10_vector_stores.py` - Work with vector stores
- **Afternoon**: `04_Vector_Stores_RAG/11_retrieval_qa.py` - Build RAG system
- **Evening**: Create a document Q&A system

### **Day 6: Agents - Basics & Tools**
- **Morning**: `05_Agents/12_agents_basic.py` - Introduction to agents
- **Afternoon**: `05_Agents/13_agent_tools.py` - Create custom tools
- **Evening**: Build an agent with custom tools

### **Day 7: Agents & Advanced Topics**
- **Morning**: `05_Agents/14_agent_executor.py` - Advanced agent execution
- **Afternoon**: `06_Advanced_Topics/15_streaming.py` - Streaming responses
- **Evening**: `06_Advanced_Topics/16_callbacks.py` - Use callbacks

### **Day 8: Advanced & Final Project**
- **Morning**: `06_Advanced_Topics/17_custom_chains.py` - Custom chains
- **Afternoon**: Plan your final project
- **Evening**: Start building your project in `07_Final_Project/`

## 🚀 Quick Start

### Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # Optional
```

### Running Examples

Navigate to the module folder and run examples:
```bash
cd 01_Basics
python 01_basic_llm.py
```

Or run from root:
```bash
python 01_Basics/01_basic_llm.py
```

## 📖 How to Use This Course

1. **Follow the 8-day plan**: Complete one day at a time
2. **Read module READMEs**: Each folder has a README with details
3. **Read code comments**: Each file has detailed explanations
4. **Experiment**: Modify the code to see how it behaves
5. **Practice**: Build small projects after each module

## 🎯 Learning Objectives

By the end of this course, you will:
- ✅ Understand LangChain's core concepts
- ✅ Build LLM applications with prompts and chains
- ✅ Implement memory in conversational AI
- ✅ Process and query documents
- ✅ Create RAG (Retrieval-Augmented Generation) systems
- ✅ Build intelligent agents with tools
- ✅ Handle streaming and callbacks
- ✅ Build a complete LangChain project

## 📝 Notes

- Most examples use OpenAI's API (requires API key)
- Some examples also support Google's Gemini (optional)
- Free alternatives like Ollama can be used for local models
- Always keep your API keys secure (use .env file)
- Each module folder has its own README with specific details

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangChain Cookbook](https://github.com/langchain-ai/langchain-cookbook)

## 📊 Progress Tracking

Track your progress:
- [ ] Day 1: Basics - LLMs & Prompts
- [ ] Day 2: Basics - Chains & Parsers
- [ ] Day 3: Memory & Conversations
- [ ] Day 4: Document Processing
- [ ] Day 5: Vector Stores & RAG
- [ ] Day 6: Agents - Basics & Tools
- [ ] Day 7: Agents & Advanced Topics
- [ ] Day 8: Advanced & Final Project

Happy Learning! 🎉
