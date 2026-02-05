"""
Module 6: Advanced Topics - Streaming Responses

This module covers:
1. What is streaming
2. Streaming LLM responses
3. Streaming chains
4. Streaming agents
5. Custom streaming handlers
"""

from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import sys

load_dotenv()

class CustomStreamHandler(BaseCallbackHandler):
    """Custom streaming callback handler"""
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated"""
        sys.stdout.write(token)
        sys.stdout.flush()

def example_basic_streaming():
    """Example of basic streaming"""
    print("=" * 60)
    print("Example 1: Basic Streaming")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Create streaming handler
    streaming_handler = StreamingStdOutCallbackHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[streaming_handler]
    )
    
    print("\nStreaming response:\n")
    response = llm.invoke("Tell me a short story about AI in 3 sentences.")
    print("\n\nStreaming complete!\n")

def example_streaming_chain():
    """Example streaming with chains"""
    print("=" * 60)
    print("Example 2: Streaming with Chains")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    streaming_handler = StreamingStdOutCallbackHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[streaming_handler]
    )
    
    prompt = ChatPromptTemplate.from_template(
        "Explain {topic} in simple terms."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    print("\nStreaming chain response:\n")
    result = chain.invoke({"topic": "quantum computing"})
    print("\n\nChain streaming complete!\n")

def example_custom_stream_handler():
    """Example with custom streaming handler"""
    print("=" * 60)
    print("Example 3: Custom Streaming Handler")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class NumberedStreamHandler(BaseCallbackHandler):
        """Handler that numbers tokens"""
        def __init__(self):
            self.token_count = 0
        
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.token_count += 1
            sys.stdout.write(f"[{self.token_count}] {token}")
            sys.stdout.flush()
    
    handler = NumberedStreamHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[handler]
    )
    
    print("\nStreaming with token numbers:\n")
    response = llm.invoke("Count from 1 to 5.")
    print(f"\n\nTotal tokens streamed: {handler.token_count}\n")

def example_streaming_with_formatting():
    """Example streaming with formatted output"""
    print("=" * 60)
    print("Example 4: Streaming with Formatting")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class FormattedStreamHandler(BaseCallbackHandler):
        """Handler that formats output"""
        def on_llm_start(self, serialized: dict, prompts: list, **kwargs) -> None:
            print("\n🤖 AI Response:\n")
        
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            sys.stdout.write(token)
            sys.stdout.flush()
        
        def on_llm_end(self, response, **kwargs) -> None:
            print("\n\n✅ Response complete!\n")
    
    handler = FormattedStreamHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[handler]
    )
    
    response = llm.invoke("What is machine learning?")

def example_streaming_multiple():
    """Example streaming multiple responses"""
    print("=" * 60)
    print("Example 5: Streaming Multiple Responses")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    streaming_handler = StreamingStdOutCallbackHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[streaming_handler]
    )
    
    questions = [
        "What is Python?",
        "What is JavaScript?",
        "What is Java?"
    ]
    
    print("\nStreaming multiple responses:\n")
    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i}: {question} ---\n")
        response = llm.invoke(question)
        print("\n")

def example_streaming_control():
    """Example controlling streaming behavior"""
    print("=" * 60)
    print("Example 6: Controlling Streaming")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class ControlledStreamHandler(BaseCallbackHandler):
        """Handler that can be paused"""
        def __init__(self, pause_after=10):
            self.token_count = 0
            self.pause_after = pause_after
        
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.token_count += 1
            sys.stdout.write(token)
            sys.stdout.flush()
            
            # Pause after certain number of tokens
            if self.token_count % self.pause_after == 0:
                print(f"\n[Paused at token {self.token_count}]")
    
    handler = ControlledStreamHandler(pause_after=15)
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True,
        callbacks=[handler]
    )
    
    print("\nStreaming with pauses:\n")
    response = llm.invoke("Write a paragraph about artificial intelligence.")
    print("\n\nStreaming complete!\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Streaming Responses")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_basic_streaming()
        example_streaming_chain()
        example_custom_stream_handler()
        example_streaming_with_formatting()
        example_streaming_multiple()
        example_streaming_control()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Streaming provides real-time responses")
        print("  - Improves user experience with faster feedback")
        print("  - Custom handlers allow formatting and control")
        print("  - Works with chains, agents, and direct LLM calls")
        print("  - Use streaming=True and callbacks for streaming\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

