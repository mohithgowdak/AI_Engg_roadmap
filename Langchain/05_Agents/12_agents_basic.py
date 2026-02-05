"""
Module 5: Agents - Introduction to Agents

This module covers:
1. What are agents
2. Basic agent setup
3. Agent types
4. Agent execution
"""

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.agents import load_tools
from dotenv import load_dotenv
import os

load_dotenv()

def example_basic_agent():
    """Example of a basic agent with tools"""
    print("=" * 60)
    print("Example 1: Basic Agent with Built-in Tools")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Load built-in tools (requires SERPAPI_API_KEY for search)
    # For this example, we'll use a simple calculator tool
    try:
        tools = load_tools(["llm-math"], llm=llm)
        
        # Create agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True  # Show agent's thinking process
        )
        
        # Run agent
        result = agent.invoke("What is 25 multiplied by 4?")
        print(f"\nResult: {result['output']}\n")
        
    except Exception as e:
        print(f"\n⚠️  Could not load tools: {e}")
        print("Note: Some tools require additional API keys.\n")

def example_agent_types():
    """Example showing different agent types"""
    print("=" * 60)
    print("Example 2: Different Agent Types")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    print("\nAgent Types:")
    print("  1. ZERO_SHOT_REACT_DESCRIPTION: Uses ReAct framework")
    print("  2. REACT_DOCSTORE: For document store interactions")
    print("  3. SELF_ASK_WITH_SEARCH: Asks follow-up questions")
    print("  4. CONVERSATIONAL_REACT_DESCRIPTION: With memory")
    print("  5. CHAT_ZERO_SHOT_REACT_DESCRIPTION: Chat-based\n")
    
    try:
        tools = load_tools(["llm-math"], llm=llm)
        
        # Conversational agent (with memory)
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=True
        )
        
        result = agent.invoke("What is 10 + 5?")
        print(f"Result: {result['output']}\n")
        
    except Exception as e:
        print(f"⚠️  Error: {e}\n")

def example_agent_reasoning():
    """Example showing agent's reasoning process"""
    print("=" * 60)
    print("Example 3: Agent Reasoning Process")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    try:
        tools = load_tools(["llm-math"], llm=llm)
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True  # This shows the reasoning
        )
        
        # Complex question that requires reasoning
        result = agent.invoke(
            "If I have 100 apples and I give away 30, then buy 50 more, how many do I have?"
        )
        print(f"\nFinal Answer: {result['output']}\n")
        
    except Exception as e:
        print(f"⚠️  Error: {e}\n")

def example_agent_with_memory():
    """Example agent with conversation memory"""
    print("=" * 60)
    print("Example 4: Agent with Memory")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    try:
        tools = load_tools(["llm-math"], llm=llm)
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=True
        )
        
        # Multi-turn conversation
        print("\nTurn 1:")
        result1 = agent.invoke("My name is Alice")
        print(f"Response: {result1['output']}\n")
        
        print("Turn 2:")
        result2 = agent.invoke("What's my name?")
        print(f"Response: {result2['output']}\n")
        
        print("Turn 3:")
        result3 = agent.invoke("Calculate 5 * 10")
        print(f"Response: {result3['output']}\n")
        
    except Exception as e:
        print(f"⚠️  Error: {e}\n")

def example_agent_error_handling():
    """Example showing how agents handle errors"""
    print("=" * 60)
    print("Example 5: Agent Error Handling")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    try:
        tools = load_tools(["llm-math"], llm=llm)
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True  # Handle parsing errors gracefully
        )
        
        # Agent will try to recover from errors
        result = agent.invoke("What is the square root of -1?")
        print(f"\nResult: {result['output']}\n")
        
    except Exception as e:
        print(f"⚠️  Error: {e}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Agents Basics")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_basic_agent()
        example_agent_types()
        example_agent_reasoning()
        example_agent_with_memory()
        example_agent_error_handling()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Agents use tools to accomplish tasks")
        print("  - Agents can reason about which tools to use")
        print("  - Different agent types for different use cases")
        print("  - Agents can have memory for conversations")
        print("  - verbose=True shows the agent's thinking process\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

