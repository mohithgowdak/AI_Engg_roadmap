"""
Module 4: Vector Stores & RAG - Retrieval-Augmented Generation (RAG)

This module covers:
1. What is RAG
2. Building a RAG chain
3. Question answering with documents
4. Improving RAG performance
5. Advanced RAG techniques
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

def example_basic_rag():
    """Example of a basic RAG system"""
    print("=" * 60)
    print("Example 1: Basic RAG System")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Create knowledge base
    knowledge_base_text = """
    LangChain is a framework for developing applications powered by language models.
    It provides standard interfaces for chains, agents, and retrieval strategies.
    
    Key components of LangChain include:
    - Chains: Combine multiple components together
    - Agents: Use tools to interact with the environment
    - Memory: Maintain conversation context
    - Document Loaders: Load from various sources
    - Vector Stores: Store and search embeddings
    
    LangChain supports multiple LLM providers including OpenAI, Anthropic, and Google.
    The framework is designed to be modular and extensible.
    """
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    
    documents = text_splitter.create_documents([knowledge_base_text])
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Create LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" means put all docs in context
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    
    # Ask questions
    questions = [
        "What is LangChain?",
        "What are the key components?",
        "Which LLM providers does it support?"
    ]
    
    print("\nAsking questions:\n")
    for question in questions:
        result = qa_chain.invoke({"query": question})
        print(f"Q: {question}")
        print(f"A: {result['result']}")
        print(f"Sources: {len(result['source_documents'])} documents\n")

def example_rag_with_custom_prompt():
    """Example RAG with custom prompt"""
    print("=" * 60)
    print("Example 2: RAG with Custom Prompt")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Sample documents
    documents = [
        Document(page_content="Python is a high-level programming language created by Guido van Rossum."),
        Document(page_content="Python supports multiple programming paradigms including OOP and functional programming."),
        Document(page_content="Python has a large standard library and many third-party packages.")
    ]
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Custom prompt template
    prompt_template = """Use the following pieces of context to answer the question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Answer in a clear and concise manner:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": "Who created Python?"})
    print(f"Q: Who created Python?")
    print(f"A: {result['result']}\n")

def example_rag_different_chain_types():
    """Example showing different chain types for RAG"""
    print("=" * 60)
    print("Example 3: Different RAG Chain Types")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Create documents
    text = """
    Machine learning is a subset of artificial intelligence.
    It involves training algorithms on data to make predictions.
    Deep learning uses neural networks with multiple layers.
    Supervised learning uses labeled data.
    Unsupervised learning finds patterns in unlabeled data.
    """ * 3
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    documents = text_splitter.create_documents([text])
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Chain types: "stuff", "map_reduce", "refine", "map_rerank"
    print("\nUsing 'stuff' chain type (all docs in context):")
    qa_stuff = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
    )
    
    result = qa_stuff.invoke({"query": "What is machine learning?"})
    print(f"Answer: {result['result'][:150]}...\n")

def example_rag_with_source_citations():
    """Example RAG that shows source documents"""
    print("=" * 60)
    print("Example 4: RAG with Source Citations")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    documents = [
        Document(
            page_content="LangChain provides tools for building LLM applications.",
            metadata={"source": "langchain_docs.txt", "page": 1}
        ),
        Document(
            page_content="Chains allow combining multiple components together.",
            metadata={"source": "langchain_docs.txt", "page": 2}
        ),
        Document(
            page_content="Agents can use tools to interact with environments.",
            metadata={"source": "langchain_docs.txt", "page": 3}
        )
    ]
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": "What can agents do?"})
    
    print(f"Q: What can agents do?")
    print(f"A: {result['result']}\n")
    print("Sources:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"  {i}. {doc.page_content[:80]}...")
        print(f"     Source: {doc.metadata}\n")

def example_rag_improved_retrieval():
    """Example with improved retrieval (more documents)"""
    print("=" * 60)
    print("Example 5: Improved Retrieval (More Context)")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Larger knowledge base
    knowledge = """
    Python is a versatile programming language used in web development, data science, and AI.
    Django and Flask are popular Python web frameworks.
    Pandas and NumPy are essential for data analysis in Python.
    TensorFlow and PyTorch are deep learning frameworks for Python.
    Python's syntax is clean and readable, making it great for beginners.
    """ * 2
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    documents = text_splitter.create_documents([knowledge])
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Retrieve more documents for better context
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Get top 5
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": "What Python libraries are used for data science?"})
    
    print(f"Q: What Python libraries are used for data science?")
    print(f"A: {result['result']}\n")
    print(f"Retrieved {len(result['source_documents'])} documents for context\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Retrieval-Augmented Generation (RAG)")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_basic_rag()
        example_rag_with_custom_prompt()
        example_rag_different_chain_types()
        example_rag_with_source_citations()
        example_rag_improved_retrieval()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - RAG combines retrieval with generation")
        print("  - RetrievalQA is the main chain for RAG")
        print("  - Custom prompts improve answer quality")
        print("  - Source documents provide citations")
        print("  - More retrieved docs = better context (but more tokens)\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

