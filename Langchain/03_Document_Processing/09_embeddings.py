"""
Module 3: Document Processing - Understanding Embeddings

This module covers:
1. What are embeddings
2. Using OpenAI embeddings
3. Using other embedding models
4. Embedding documents
5. Similarity search with embeddings
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def example_openai_embeddings():
    """Example using OpenAI embeddings"""
    print("=" * 60)
    print("Example 1: OpenAI Embeddings")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return None
    
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # Embed a single text
    text = "LangChain is a framework for LLM applications"
    embedding = embeddings.embed_query(text)
    
    print(f"\nText: {text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}\n")
    
    return embeddings

def example_embed_multiple_texts():
    """Example embedding multiple texts"""
    print("=" * 60)
    print("Example 2: Embedding Multiple Texts")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    texts = [
        "Python is a programming language",
        "Machine learning uses algorithms",
        "LangChain helps build LLM apps",
        "Data science involves statistics"
    ]
    
    # Embed multiple texts at once
    text_embeddings = embeddings.embed_documents(texts)
    
    print(f"\nEmbedded {len(texts)} texts")
    print(f"Each embedding has {len(text_embeddings[0])} dimensions\n")
    
    for i, (text, emb) in enumerate(zip(texts, text_embeddings), 1):
        print(f"Text {i}: {text}")
        print(f"  Embedding norm: {np.linalg.norm(emb):.4f}\n")

def example_embed_documents():
    """Example embedding Document objects"""
    print("=" * 60)
    print("Example 3: Embedding Documents")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    documents = [
        Document(page_content="Python programming basics", metadata={"topic": "programming"}),
        Document(page_content="Machine learning fundamentals", metadata={"topic": "ML"}),
        Document(page_content="Data analysis techniques", metadata={"topic": "data"})
    ]
    
    # Extract texts from documents
    texts = [doc.page_content for doc in documents]
    doc_embeddings = embeddings.embed_documents(texts)
    
    print(f"\nEmbedded {len(documents)} documents\n")
    for i, (doc, emb) in enumerate(zip(documents, doc_embeddings), 1):
        print(f"Doc {i}: {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
        print(f"  Embedding shape: {len(emb)}\n")

def example_similarity_search():
    """Example finding similar texts using embeddings"""
    print("=" * 60)
    print("Example 4: Similarity Search with Embeddings")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # Knowledge base
    knowledge_base = [
        "Python is a high-level programming language",
        "Machine learning is a subset of artificial intelligence",
        "LangChain is a framework for building LLM applications",
        "Neural networks are used in deep learning",
        "Data science combines statistics and programming"
    ]
    
    # Query
    query = "What is artificial intelligence?"
    
    # Embed everything
    kb_embeddings = embeddings.embed_documents(knowledge_base)
    query_embedding = embeddings.embed_query(query)
    
    # Calculate cosine similarity
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    similarities = [cosine_similarity(query_embedding, kb_emb) for kb_emb in kb_embeddings]
    
    # Find most similar
    most_similar_idx = np.argmax(similarities)
    
    print(f"\nQuery: {query}")
    print(f"\nMost similar text:")
    print(f"  {knowledge_base[most_similar_idx]}")
    print(f"  Similarity: {similarities[most_similar_idx]:.4f}\n")
    
    # Show all similarities
    print("All similarities:")
    for i, (text, sim) in enumerate(zip(knowledge_base, similarities), 1):
        print(f"  {i}. {sim:.4f} - {text}")

def example_huggingface_embeddings():
    """Example using HuggingFace embeddings (free alternative)"""
    print("=" * 60)
    print("Example 5: HuggingFace Embeddings (Free Alternative)")
    print("=" * 60)
    
    try:
        # Use a lightweight model (downloads on first use)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        text = "LangChain is a framework for LLM applications"
        embedding = embeddings.embed_query(text)
        
        print(f"\nText: {text}")
        print(f"Embedding dimension: {len(embedding)}")
        print(f"First 10 values: {embedding[:10]}\n")
        print("✅ HuggingFace embeddings work without API key!\n")
        
    except Exception as e:
        print(f"\n⚠️  Could not load HuggingFace embeddings: {e}")
        print("You may need to install: pip install sentence-transformers\n")

def example_embedding_comparison():
    """Example comparing embeddings of similar texts"""
    print("=" * 60)
    print("Example 6: Comparing Embeddings")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # Similar texts should have similar embeddings
    text1 = "Python is a programming language"
    text2 = "Python is a coding language"  # Similar meaning
    text3 = "The weather is sunny today"  # Different topic
    
    emb1 = embeddings.embed_query(text1)
    emb2 = embeddings.embed_query(text2)
    emb3 = embeddings.embed_query(text3)
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    sim_1_2 = cosine_similarity(emb1, emb2)
    sim_1_3 = cosine_similarity(emb1, emb3)
    
    print(f"\nText 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Text 3: {text3}\n")
    
    print(f"Similarity between 1 and 2: {sim_1_2:.4f} (should be high)")
    print(f"Similarity between 1 and 3: {sim_1_3:.4f} (should be low)\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Embeddings")
    print("=" * 60 + "\n")
    
    try:
        example_openai_embeddings()
        example_embed_multiple_texts()
        example_embed_documents()
        example_similarity_search()
        example_huggingface_embeddings()
        example_embedding_comparison()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Embeddings convert text to numerical vectors")
        print("  - Similar texts have similar embeddings")
        print("  - Embeddings enable semantic search")
        print("  - OpenAI embeddings are high quality but require API key")
        print("  - HuggingFace provides free alternatives\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

