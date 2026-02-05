"""
Module 3: Document Processing - Text Splitters

This module covers:
1. Why split documents
2. CharacterTextSplitter
3. RecursiveCharacterTextSplitter
4. TokenTextSplitter
5. Custom splitting strategies
"""

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

def example_character_splitter():
    """Example using CharacterTextSplitter"""
    print("=" * 60)
    print("Example 1: Character Text Splitter")
    print("=" * 60)
    
    # Create a sample long document
    long_text = """
    LangChain is a framework for developing applications powered by language models.
    It provides standard interfaces for chains, agents, and retrieval strategies.
    LangChain enables applications that are context-aware and can reason about answers.
    The framework supports multiple LLM providers and includes tools for document processing.
    You can build chatbots, Q&A systems, and agentic applications with LangChain.
    """ * 5  # Repeat to make it longer
    
    # Split by character count
    text_splitter = CharacterTextSplitter(
        separator="\n",  # Split on newlines
        chunk_size=200,  # Maximum characters per chunk
        chunk_overlap=50,  # Overlap between chunks (for context)
        length_function=len
    )
    
    chunks = text_splitter.split_text(long_text)
    
    print(f"\nOriginal text length: {len(long_text)} characters")
    print(f"Split into {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
        print(f"Chunk {i} ({len(chunk)} chars):")
        print(f"  {chunk[:100]}...\n")

def example_recursive_splitter():
    """Example using RecursiveCharacterTextSplitter (recommended)"""
    print("=" * 60)
    print("Example 2: Recursive Character Text Splitter (Recommended)")
    print("=" * 60)
    
    # Sample document
    sample_doc = """
    # Introduction to LangChain
    
    LangChain is a powerful framework for building LLM applications.
    
    ## Key Features
    
    - Chains: Combine multiple components
    - Agents: Use tools to interact with environment
    - Memory: Maintain conversation context
    - Document Loaders: Load from various sources
    
    ## Getting Started
    
    To get started with LangChain, you need to install it first.
    Then you can create chains and agents for your applications.
    """ * 3
    
    # Recursive splitter tries to keep related content together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]  # Try these in order
    )
    
    chunks = text_splitter.split_text(sample_doc)
    
    print(f"\nSplit into {len(chunks)} chunks\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(f"  {chunk.strip()}\n")

def example_split_documents():
    """Example splitting Document objects"""
    print("=" * 60)
    print("Example 3: Splitting Document Objects")
    print("=" * 60)
    
    # Create documents
    documents = [
        Document(
            page_content="This is the first document. It contains information about Python.",
            metadata={"source": "doc1.txt", "page": 1}
        ),
        Document(
            page_content="This is the second document. It contains information about machine learning.",
            metadata={"source": "doc2.txt", "page": 1}
        ),
        Document(
            page_content="This is a longer document that needs to be split. " * 10,
            metadata={"source": "doc3.txt", "page": 1}
        )
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    
    # Split documents
    split_docs = text_splitter.split_documents(documents)
    
    print(f"\nOriginal: {len(documents)} documents")
    print(f"After splitting: {len(split_docs)} documents\n")
    
    for i, doc in enumerate(split_docs[:5], 1):  # Show first 5
        print(f"Split Doc {i}:")
        print(f"  Content: {doc.page_content[:80]}...")
        print(f"  Metadata: {doc.metadata}\n")

def example_token_splitter():
    """Example using TokenTextSplitter (for token-aware splitting)"""
    print("=" * 60)
    print("Example 4: Token Text Splitter")
    print("=" * 60)
    
    # Token splitter is useful when you need to respect token limits
    text_splitter = TokenTextSplitter(
        chunk_size=50,  # Maximum tokens per chunk
        chunk_overlap=10  # Overlap in tokens
    )
    
    text = """
    LangChain provides tools for building LLM applications.
    It supports multiple providers and includes document processing.
    You can create chains, agents, and retrieval systems.
    """ * 5
    
    chunks = text_splitter.split_text(text)
    
    print(f"\nSplit into {len(chunks)} chunks (token-aware)\n")
    for i, chunk in enumerate(chunks[:3], 1):
        print(f"Chunk {i}:")
        print(f"  {chunk[:100]}...\n")

def example_custom_splitter():
    """Example creating a custom splitting strategy"""
    print("=" * 60)
    print("Example 5: Custom Splitting Strategy")
    print("=" * 60)
    
    # Custom splitter for code-like content
    class CodeSplitter(CharacterTextSplitter):
        def __init__(self, **kwargs):
            super().__init__(
                separator="\n\n",  # Split on double newlines (paragraphs)
                **kwargs
            )
    
    code_text = """
    def hello_world():
        print("Hello, World!")
    
    def calculate_sum(a, b):
        return a + b
    
    def process_data(data):
        result = []
        for item in data:
            result.append(item * 2)
        return result
    """ * 3
    
    splitter = CodeSplitter(chunk_size=150, chunk_overlap=30)
    chunks = splitter.split_text(code_text)
    
    print(f"\nSplit code into {len(chunks)} chunks\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(f"  {chunk.strip()}\n")

def example_splitting_with_metadata():
    """Example preserving metadata when splitting"""
    print("=" * 60)
    print("Example 6: Splitting with Metadata Preservation")
    print("=" * 60)
    
    document = Document(
        page_content="This is a long document that needs to be split. " * 20,
        metadata={"source": "important_doc.txt", "author": "John Doe", "date": "2024-01-01"}
    )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    
    split_docs = text_splitter.split_documents([document])
    
    print(f"\nOriginal document metadata: {document.metadata}")
    print(f"Split into {len(split_docs)} chunks\n")
    
    # All chunks preserve the original metadata
    for i, doc in enumerate(split_docs[:3], 1):
        print(f"Chunk {i} metadata: {doc.metadata}")
        print(f"  Content: {doc.page_content[:60]}...\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Text Splitters")
    print("=" * 60 + "\n")
    
    try:
        example_character_splitter()
        example_recursive_splitter()
        example_split_documents()
        example_token_splitter()
        example_custom_splitter()
        example_splitting_with_metadata()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Split documents to fit LLM context windows")
        print("  - RecursiveCharacterTextSplitter is recommended")
        print("  - Use chunk_overlap to maintain context")
        print("  - Metadata is preserved when splitting documents")
        print("  - Choose splitter based on your document type\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

