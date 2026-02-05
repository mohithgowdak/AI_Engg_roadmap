"""
Module 4: Vector Stores & RAG - Working with Vector Stores

This module covers:
1. What are vector stores
2. Using Chroma (in-memory)
3. Using FAISS
4. Adding documents to vector stores
5. Querying vector stores
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

def example_chroma_basic():
    """Example using Chroma vector store"""
    print("=" * 60)
    print("Example 1: Chroma Vector Store (Basic)")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return None
    
    embeddings = OpenAIEmbeddings()
    
    # Create sample documents
    documents = [
        Document(page_content="Python is a high-level programming language"),
        Document(page_content="Machine learning is a subset of AI"),
        Document(page_content="LangChain helps build LLM applications"),
        Document(page_content="Data science combines statistics and programming")
    ]
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=None  # In-memory (use path to persist)
    )
    
    print(f"\nCreated vector store with {len(documents)} documents")
    
    # Query the vector store
    query = "What is Python?"
    results = vectorstore.similarity_search(query, k=2)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} similar documents:\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content}\n")
    
    return vectorstore

def example_faiss_basic():
    """Example using FAISS vector store"""
    print("=" * 60)
    print("Example 2: FAISS Vector Store")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return None
    
    embeddings = OpenAIEmbeddings()
    
    documents = [
        Document(page_content="Neural networks are inspired by the brain"),
        Document(page_content="Deep learning uses multiple layers"),
        Document(page_content="Convolutional networks are for images"),
        Document(page_content="Recurrent networks handle sequences")
    ]
    
    # Create FAISS vector store
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    print(f"\nCreated FAISS vector store with {len(documents)} documents")
    
    # Similarity search with scores
    query = "How do neural networks work?"
    results = vectorstore.similarity_search_with_score(query, k=2)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} results:\n")
    for i, (doc, score) in enumerate(results, 1):
        print(f"{i}. Score: {score:.4f}")
        print(f"   Content: {doc.page_content}\n")
    
    return vectorstore

def example_add_documents():
    """Example adding documents to existing vector store"""
    print("=" * 60)
    print("Example 3: Adding Documents to Vector Store")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings()
    
    # Initial documents
    initial_docs = [
        Document(page_content="Python is versatile"),
        Document(page_content="JavaScript is for web development")
    ]
    
    vectorstore = FAISS.from_documents(initial_docs, embeddings)
    print(f"Initial documents: {len(initial_docs)}")
    
    # Add more documents
    new_docs = [
        Document(page_content="Java is object-oriented"),
        Document(page_content="C++ is for system programming")
    ]
    
    vectorstore.add_documents(new_docs)
    print(f"After adding: {vectorstore.index.ntotal} documents\n")
    
    # Query
    results = vectorstore.similarity_search("programming languages", k=3)
    print("Query: 'programming languages'")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")

def example_persist_vectorstore():
    """Example persisting and loading vector store"""
    print("=" * 60)
    print("Example 4: Persisting Vector Store")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings()
    
    documents = [
        Document(page_content="Vector stores enable semantic search"),
        Document(page_content="Embeddings capture meaning in vectors")
    ]
    
    # Create and persist
    persist_dir = "./vector_db"
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    
    print(f"\nSaved vector store to {persist_dir}")
    
    # Load from disk
    loaded_vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    
    print(f"Loaded vector store with {loaded_vectorstore._collection.count()} documents")
    
    # Clean up
    import shutil
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
        print("Cleaned up persisted directory\n")

def example_metadata_filtering():
    """Example using metadata to filter search results"""
    print("=" * 60)
    print("Example 5: Metadata Filtering")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings()
    
    # Documents with metadata
    documents = [
        Document(
            page_content="Python is great for data science",
            metadata={"category": "programming", "level": "beginner"}
        ),
        Document(
            page_content="Machine learning algorithms",
            metadata={"category": "ML", "level": "intermediate"}
        ),
        Document(
            page_content="Advanced neural networks",
            metadata={"category": "ML", "level": "advanced"}
        ),
        Document(
            page_content="Python web frameworks",
            metadata={"category": "programming", "level": "intermediate"}
        )
    ]
    
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Search without filter
    print("Search without filter:")
    results = vectorstore.similarity_search("Python", k=2)
    for doc in results:
        print(f"  {doc.page_content} - {doc.metadata}\n")
    
    # Search with metadata filter (FAISS doesn't support filtering directly)
    # But we can filter results after retrieval
    print("Filtered results (programming category):")
    results = vectorstore.similarity_search("Python", k=4)
    filtered = [doc for doc in results if doc.metadata.get("category") == "programming"]
    for doc in filtered:
        print(f"  {doc.page_content} - {doc.metadata}\n")

def example_similarity_search_vs_mmr():
    """Example comparing similarity search vs MMR"""
    print("=" * 60)
    print("Example 6: Similarity Search vs MMR (Maximal Marginal Relevance)")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings()
    
    # Create diverse documents
    documents = [
        Document(page_content="Python is a programming language"),
        Document(page_content="Python has many libraries"),
        Document(page_content="Machine learning uses Python"),
        Document(page_content="Data science relies on Python"),
        Document(page_content="JavaScript is another language"),
        Document(page_content="Java is object-oriented")
    ]
    
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    query = "Python programming"
    
    # Standard similarity search (may return similar results)
    print("Standard Similarity Search (may have duplicates):")
    results = vectorstore.similarity_search(query, k=4)
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    
    # MMR search (diverse results)
    print("\nMMR Search (diverse results):")
    results = vectorstore.max_marginal_relevance_search(query, k=4, fetch_k=6)
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Vector Stores")
    print("=" * 60 + "\n")
    
    try:
        example_chroma_basic()
        example_faiss_basic()
        example_add_documents()
        example_persist_vectorstore()
        example_metadata_filtering()
        example_similarity_search_vs_mmr()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Vector stores enable semantic search")
        print("  - Chroma is good for persistence")
        print("  - FAISS is fast and efficient")
        print("  - You can add documents dynamically")
        print("  - MMR provides diverse search results\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

