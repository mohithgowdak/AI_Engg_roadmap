"""
Module 2: Memory & Conversations - Basic Memory Concepts

This module covers:
1. What is memory in LangChain
2. Different types of memory
3. ConversationBufferMemory
4. ConversationBufferWindowMemory
"""

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

load_dotenv()

def example_buffer_memory():
    """Example using ConversationBufferMemory (remembers everything)"""
    print("=" * 60)
    print("Example 1: Conversation Buffer Memory")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create memory that stores all conversation history
    memory = ConversationBufferMemory(
        return_messages=True,  # Return messages instead of string
        memory_key="history"   # Key to store history
    )
    
    # Create a prompt that includes memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Create a chain with memory
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    # Have a conversation
    print("\nStarting conversation...\n")
    
    response1 = chain.invoke({"input": "My name is Alice"})
    print(f"User: My name is Alice")
    print(f"AI: {response1['response']}\n")
    
    response2 = chain.invoke({"input": "What's my name?"})
    print(f"User: What's my name?")
    print(f"AI: {response2['response']}\n")
    
    # Show memory contents
    print("Memory contents:")
    print(memory.chat_memory.messages)
    print()

def example_window_memory():
    """Example using ConversationBufferWindowMemory (remembers last N messages)"""
    print("=" * 60)
    print("Example 2: Conversation Buffer Window Memory")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Memory that only keeps last k messages (k=2 in this case)
    memory = ConversationBufferWindowMemory(
        k=2,  # Keep only last 2 exchanges
        return_messages=True
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    print("\nHaving a conversation (memory keeps last 2 exchanges)...\n")
    
    chain.invoke({"input": "I like Python"})
    chain.invoke({"input": "I also like JavaScript"})
    chain.invoke({"input": "What programming languages do I like?"})
    
    # The memory should only remember the last 2 exchanges
    print(f"\nMemory has {len(memory.chat_memory.messages)} messages")
    print()

def example_summary_memory():
    """Example using ConversationSummaryMemory (summarizes old conversations)"""
    print("=" * 60)
    print("Example 3: Conversation Summary Memory")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Memory that summarizes old conversations to save tokens
    memory = ConversationSummaryMemory(
        llm=llm,
        return_messages=True
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    print("\nHaving a long conversation (old parts will be summarized)...\n")
    
    # Simulate a longer conversation
    messages = [
        "I'm learning Python",
        "I want to build web applications",
        "What framework should I use?",
        "Tell me about Django",
        "What about Flask?",
        "Which one is better for beginners?"
    ]
    
    for msg in messages:
        response = chain.invoke({"input": msg})
        print(f"User: {msg}")
        print(f"AI: {response['response'][:100]}...\n")
    
    print("Memory summary created to save tokens!")
    print()

def example_memory_operations():
    """Example showing memory operations (save, load, clear)"""
    print("=" * 60)
    print("Example 4: Memory Operations")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    memory = ConversationBufferMemory(return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )
    
    # Add some conversation
    chain.invoke({"input": "My favorite color is blue"})
    chain.invoke({"input": "I love reading books"})
    
    print(f"Memory before clearing: {len(memory.chat_memory.messages)} messages")
    
    # Clear memory
    memory.clear()
    print(f"Memory after clearing: {len(memory.chat_memory.messages)} messages")
    
    # The AI won't remember previous conversation
    response = chain.invoke({"input": "What's my favorite color?"})
    print(f"\nUser: What's my favorite color?")
    print(f"AI: {response['response']}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Memory Basics")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_buffer_memory()
        example_window_memory()
        example_summary_memory()
        example_memory_operations()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - BufferMemory: Remembers everything (can be expensive)")
        print("  - WindowMemory: Remembers last N messages (efficient)")
        print("  - SummaryMemory: Summarizes old conversations (best for long chats)")
        print("  - Memory allows LLMs to have context in conversations\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

