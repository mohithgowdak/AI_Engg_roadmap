"""
Module 6: Advanced Topics - Using Callbacks

This module covers:
1. What are callbacks
2. Built-in callbacks
3. Custom callbacks
4. Callback handlers
5. Monitoring and logging
"""

from langchain_openai import ChatOpenAI
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from typing import Any, Dict, List

load_dotenv()

class TokenCounterCallback(BaseCallbackHandler):
    """Custom callback to count tokens"""
    def __init__(self):
        self.token_count = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Called when LLM starts"""
        print(f"[Callback] LLM started with {len(prompts)} prompt(s)")
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Called when a new token is generated"""
        self.token_count += 1
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Called when LLM finishes"""
        if response.llm_output and 'token_usage' in response.llm_output:
            usage = response.llm_output['token_usage']
            self.prompt_tokens = usage.get('prompt_tokens', 0)
            self.completion_tokens = usage.get('completion_tokens', 0)
            print(f"[Callback] LLM finished")
            print(f"  Prompt tokens: {self.prompt_tokens}")
            print(f"  Completion tokens: {self.completion_tokens}")
            print(f"  Total tokens: {usage.get('total_tokens', 0)}")

def example_stdout_callback():
    """Example using StdOutCallbackHandler"""
    print("=" * 60)
    print("Example 1: StdOut Callback Handler")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Standard output callback
    callback = StdOutCallbackHandler()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        callbacks=[callback]
    )
    
    print("\nUsing stdout callback:\n")
    response = llm.invoke("What is Python?")
    print(f"\nResponse: {response.content[:100]}...\n")

def example_custom_callback():
    """Example creating custom callback"""
    print("=" * 60)
    print("Example 2: Custom Callback")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class SimpleCallback(BaseCallbackHandler):
        """Simple custom callback"""
        def on_llm_start(self, serialized, prompts, **kwargs):
            print("🚀 LLM call started!")
        
        def on_llm_end(self, response, **kwargs):
            print("✅ LLM call completed!")
        
        def on_llm_error(self, error, **kwargs):
            print(f"❌ LLM error: {error}")
    
    callback = SimpleCallback()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        callbacks=[callback]
    )
    
    response = llm.invoke("Tell me about AI")
    print(f"\nResponse: {response.content[:100]}...\n")

def example_token_counter_callback():
    """Example callback that counts tokens"""
    print("=" * 60)
    print("Example 3: Token Counter Callback")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    token_counter = TokenCounterCallback()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        callbacks=[token_counter]
    )
    
    print("\nMaking LLM call with token counter:\n")
    response = llm.invoke("Explain machine learning in detail.")
    print(f"\nResponse length: {len(response.content)} characters\n")

def example_chain_callbacks():
    """Example using callbacks with chains"""
    print("=" * 60)
    print("Example 4: Callbacks with Chains")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class ChainCallback(BaseCallbackHandler):
        """Callback for chain execution"""
        def on_chain_start(self, serialized, inputs, **kwargs):
            print(f"[Chain] Started: {serialized.get('name', 'Unknown')}")
        
        def on_chain_end(self, outputs, **kwargs):
            print(f"[Chain] Completed")
        
        def on_chain_error(self, error, **kwargs):
            print(f"[Chain] Error: {error}")
    
    callback = ChainCallback()
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    prompt = ChatPromptTemplate.from_template("Explain {topic}")
    chain = LLMChain(llm=llm, prompt=prompt)
    
    print("\nRunning chain with callback:\n")
    result = chain.invoke({"topic": "blockchain"}, callbacks=[callback])
    print(f"\nResult: {result['text'][:100]}...\n")

def example_multiple_callbacks():
    """Example using multiple callbacks"""
    print("=" * 60)
    print("Example 5: Multiple Callbacks")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class LoggerCallback(BaseCallbackHandler):
        """Callback that logs events"""
        def on_llm_start(self, serialized, prompts, **kwargs):
            print("[Logger] LLM call initiated")
        
        def on_llm_end(self, response, **kwargs):
            print("[Logger] LLM call finished")
    
    class TimerCallback(BaseCallbackHandler):
        """Callback that times execution"""
        def __init__(self):
            import time
            self.start_time = None
            self.time_module = time
        
        def on_llm_start(self, serialized, prompts, **kwargs):
            self.start_time = self.time_module.time()
        
        def on_llm_end(self, response, **kwargs):
            if self.start_time:
                elapsed = self.time_module.time() - self.start_time
                print(f"[Timer] Execution took {elapsed:.2f} seconds")
    
    logger = LoggerCallback()
    timer = TimerCallback()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        callbacks=[logger, timer]
    )
    
    print("\nUsing multiple callbacks:\n")
    response = llm.invoke("What is data science?")
    print(f"\nResponse: {response.content[:100]}...\n")

def example_callback_with_data():
    """Example callback that collects data"""
    print("=" * 60)
    print("Example 6: Callback with Data Collection")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class DataCollectorCallback(BaseCallbackHandler):
        """Callback that collects execution data"""
        def __init__(self):
            self.data = {
                "calls": 0,
                "total_tokens": 0,
                "errors": 0
            }
        
        def on_llm_start(self, serialized, prompts, **kwargs):
            self.data["calls"] += 1
        
        def on_llm_end(self, response, **kwargs):
            if response.llm_output and 'token_usage' in response.llm_output:
                tokens = response.llm_output['token_usage'].get('total_tokens', 0)
                self.data["total_tokens"] += tokens
        
        def on_llm_error(self, error, **kwargs):
            self.data["errors"] += 1
        
        def get_stats(self):
            return self.data
    
    collector = DataCollectorCallback()
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        callbacks=[collector]
    )
    
    # Make multiple calls
    print("\nMaking multiple LLM calls:\n")
    for i in range(3):
        response = llm.invoke(f"Tell me fact {i+1} about Python")
        print(f"Call {i+1} completed\n")
    
    # Show collected stats
    stats = collector.get_stats()
    print("Collected Statistics:")
    print(f"  Total calls: {stats['calls']}")
    print(f"  Total tokens: {stats['total_tokens']}")
    print(f"  Errors: {stats['errors']}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Callbacks")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_stdout_callback()
        example_custom_callback()
        example_token_counter_callback()
        example_chain_callbacks()
        example_multiple_callbacks()
        example_callback_with_data()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Callbacks allow monitoring LLM execution")
        print("  - Custom callbacks can collect metrics and logs")
        print("  - Multiple callbacks can be used together")
        print("  - Callbacks work with chains, agents, and LLMs")
        print("  - Useful for debugging and monitoring production apps\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

