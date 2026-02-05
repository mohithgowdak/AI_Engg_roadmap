"""
Module 3: Document Processing - Loading Documents

This module covers:
1. Loading text files
2. Loading PDFs
3. Loading web pages
4. Loading from URLs
5. Loading structured data
"""

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader, CSVLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv()

def example_text_loader():
    """Example loading a text file"""
    print("=" * 60)
    print("Example 1: Loading Text Files")
    print("=" * 60)
    
    # Create a sample text file for demonstration
    sample_text = """LangChain is a framework for developing applications powered by language models.
    
It enables applications that:
- Are context-aware: connect a language model to sources of context
- Are reasoning: rely on a language model to reason about how to answer

LangChain provides standard interfaces for chains, agents, and retrieval strategies."""
    
    # Write sample file
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    # Load the text file
    loader = TextLoader("sample.txt", encoding="utf-8")
    documents = loader.load()
    
    print(f"\nLoaded {len(documents)} document(s)")
    print(f"Document content (first 200 chars):")
    print(documents[0].page_content[:200])
    print(f"\nMetadata: {documents[0].metadata}\n")
    
    # Clean up
    os.remove("sample.txt")

def example_pdf_loader():
    """Example loading a PDF file"""
    print("=" * 60)
    print("Example 2: Loading PDF Files")
    print("=" * 60)
    
    print("\nNote: This example requires a PDF file.")
    print("To test, create a PDF file or use an existing one.\n")
    
    # Example code (commented out as we don't have a PDF)
    # loader = PyPDFLoader("example.pdf")
    # documents = loader.load()
    # 
    # print(f"Loaded {len(documents)} pages")
    # for i, doc in enumerate(documents[:3], 1):  # Show first 3 pages
    #     print(f"\nPage {i}:")
    #     print(doc.page_content[:200])
    
    print("PDF loader usage:")
    print("  loader = PyPDFLoader('path/to/file.pdf')")
    print("  documents = loader.load()")
    print("  # Each page becomes a separate document\n")

def example_web_loader():
    """Example loading content from a web page"""
    print("=" * 60)
    print("Example 3: Loading Web Pages")
    print("=" * 60)
    
    try:
        # Load content from a web page
        loader = WebBaseLoader("https://python.langchain.com/docs/get_started/introduction")
        documents = loader.load()
        
        print(f"\nLoaded {len(documents)} document(s) from web")
        print(f"Content preview (first 300 chars):")
        print(documents[0].page_content[:300])
        print(f"\nSource: {documents[0].metadata.get('source', 'N/A')}\n")
    except Exception as e:
        print(f"\n⚠️  Could not load web page: {e}")
        print("This might be due to network issues or the URL being unavailable.\n")

def example_csv_loader():
    """Example loading CSV files"""
    print("=" * 60)
    print("Example 4: Loading CSV Files")
    print("=" * 60)
    
    # Create a sample CSV file
    sample_csv = """name,age,city
Alice,30,New York
Bob,25,San Francisco
Charlie,35,Chicago"""
    
    with open("sample.csv", "w", encoding="utf-8") as f:
        f.write(sample_csv)
    
    # Load CSV
    loader = CSVLoader("sample.csv")
    documents = loader.load()
    
    print(f"\nLoaded {len(documents)} row(s) from CSV")
    for i, doc in enumerate(documents, 1):
        print(f"\nRow {i}:")
        print(f"  Content: {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
    
    # Clean up
    os.remove("sample.csv")
    print()

def example_directory_loader():
    """Example loading all files from a directory"""
    print("=" * 60)
    print("Example 5: Loading from Directory")
    print("=" * 60)
    
    # Create a sample directory with multiple files
    os.makedirs("sample_docs", exist_ok=True)
    
    files = {
        "doc1.txt": "This is the first document about Python programming.",
        "doc2.txt": "This is the second document about machine learning.",
        "doc3.txt": "This is the third document about data science."
    }
    
    for filename, content in files.items():
        with open(f"sample_docs/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
    
    # Load all text files from directory
    loader = DirectoryLoader(
        "sample_docs",
        glob="*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    
    print(f"\nLoaded {len(documents)} document(s) from directory")
    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i}:")
        print(f"  Content: {doc.page_content}")
        print(f"  Source: {doc.metadata.get('source', 'N/A')}")
    
    # Clean up
    import shutil
    shutil.rmtree("sample_docs")
    print()

def example_custom_document():
    """Example creating custom documents"""
    print("=" * 60)
    print("Example 6: Creating Custom Documents")
    print("=" * 60)
    
    # Create documents manually
    documents = [
        Document(
            page_content="LangChain is a powerful framework for LLM applications.",
            metadata={"source": "manual", "topic": "introduction"}
        ),
        Document(
            page_content="Chains allow you to combine multiple components together.",
            metadata={"source": "manual", "topic": "chains"}
        ),
        Document(
            page_content="Agents can use tools to interact with the environment.",
            metadata={"source": "manual", "topic": "agents"}
        )
    ]
    
    print(f"\nCreated {len(documents)} custom document(s)")
    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i}:")
        print(f"  Content: {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
    print()

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Document Loaders")
    print("=" * 60 + "\n")
    
    try:
        example_text_loader()
        example_pdf_loader()
        example_web_loader()
        example_csv_loader()
        example_directory_loader()
        example_custom_document()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Document loaders read from various sources")
        print("  - Each document has page_content and metadata")
        print("  - You can load from files, web, directories, etc.")
        print("  - Documents are the foundation for RAG systems\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

