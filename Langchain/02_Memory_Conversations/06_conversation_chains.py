"""
Module 2: Memory & Conversations - Conversation Chains

This module shows practical examples of:
1. Building chatbots with memory
2. ConversationChain usage
3. Custom conversation flows
4. Multi-turn conversations
"""

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

load_dotenv()

def example_simple_chatbot():
    """Example of a simple chatbot with memory"""
    print("=" * 60)
    print("Example 1: Simple Chatbot")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly and helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    print("\n🤖 Chatbot started! (Type 'quit' to exit)\n")
    
    # Simulate conversation
    conversations = [
        "Hello!",
        "Can you help me learn Python?",
        "What's the best way to start?",
        "Thanks for the advice!"
    ]
    
    for user_input in conversations:
        response = chain.invoke({"input": user_input})
        print(f"👤 You: {user_input}")
        print(f"🤖 Bot: {response['response']}\n")

def example_contextual_chatbot():
    """Example chatbot that maintains context across turns"""
    print("=" * 60)
    print("Example 2: Contextual Chatbot")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful coding tutor. 
        Remember what the user tells you and refer back to it in future responses.
        Be encouraging and provide clear explanations."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )
    
    print("\nStarting contextual conversation...\n")
    
    # Multi-turn conversation with context
    turns = [
        "I'm a beginner programmer",
        "I want to learn web development",
        "What should I learn first?",
        "Can you give me a simple example?",
        "Explain that example in more detail"
    ]
    
    for turn in turns:
        response = chain.invoke({"input": turn})
        print(f"User: {turn}")
        print(f"Tutor: {response['response'][:150]}...\n")

def example_summary_buffer_memory():
    """Example using ConversationSummaryBufferMemory (hybrid approach)"""
    print("=" * 60)
    print("Example 3: Summary Buffer Memory (Best of Both Worlds)")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # This memory keeps recent messages but summarizes older ones
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=100,  # When exceeded, older messages are summarized
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
    
    print("\nLong conversation (older parts will be summarized)...\n")
    
    # Simulate a long conversation
    long_conversation = [
        "I'm planning a trip to Japan",
        "I want to visit Tokyo",
        "What are the best places to see?",
        "I also want to see Kyoto",
        "How many days should I spend in each city?",
        "What about food recommendations?",
        "Can you create an itinerary?",
        "What's the best time to visit?"
    ]
    
    for i, msg in enumerate(long_conversation, 1):
        response = chain.invoke({"input": msg})
        print(f"Turn {i}: {msg}")
        print(f"Response: {response['response'][:100]}...\n")
        if i % 3 == 0:
            print("(Memory may be summarizing older messages now...)\n")

def example_specialized_chatbot():
    """Example of a specialized chatbot (e.g., customer service)"""
    print("=" * 60)
    print("Example 4: Specialized Chatbot (Customer Service)")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)  # Lower temp for consistency
    memory = ConversationBufferMemory(return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a customer service representative for an online store.
        Be polite, professional, and helpful.
        Remember customer details like name, order number, and issues.
        Always try to resolve issues efficiently."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )
    
    print("\nCustomer service conversation...\n")
    
    service_conversation = [
        "Hi, I need help with my order",
        "My order number is ORD-12345",
        "I haven't received it yet",
        "It's been 2 weeks",
        "Can you check the status?",
        "Thank you for your help"
    ]
    
    for msg in service_conversation:
        response = chain.invoke({"input": msg})
        print(f"Customer: {msg}")
        print(f"Agent: {response['response'][:150]}...\n")

def example_conversation_with_variables():
    """Example showing how to use variables in conversation chains"""
    print("=" * 60)
    print("Example 5: Conversation with Additional Variables")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. User's name: {user_name}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )
    
    print("\nConversation with user context...\n")
    
    # First set the user name
    response1 = chain.invoke({
        "input": "Hello!",
        "user_name": "Alice"
    })
    print(f"User (Alice): Hello!")
    print(f"AI: {response1['response'][:100]}...\n")
    
    # Continue conversation (user_name persists in memory context)
    response2 = chain.invoke({
        "input": "What's my name?",
        "user_name": "Alice"  # Still need to provide it
    })
    print(f"User: What's my name?")
    print(f"AI: {response2['response']}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Conversation Chains")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_simple_chatbot()
        example_contextual_chatbot()
        example_summary_buffer_memory()
        example_specialized_chatbot()
        example_conversation_with_variables()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - ConversationChain makes it easy to build chatbots")
        print("  - Memory allows maintaining context across turns")
        print("  - Choose memory type based on conversation length")
        print("  - System prompts define the chatbot's personality\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

