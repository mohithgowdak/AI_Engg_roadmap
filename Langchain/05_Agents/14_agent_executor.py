"""
Module 5: Agents - Advanced Agent Execution

This module covers:
1. Agent executors
2. Custom agent executors
3. Agent callbacks
4. Error handling
5. Agent debugging
"""

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

def example_agent_executor():
    """Example using AgentExecutor directly"""
    print("=" * 60)
    print("Example 1: Agent Executor")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @Tool
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    @Tool
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [multiply, add]
    
    # Create agent using initialize_agent (returns AgentExecutor)
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,  # Limit iterations
        max_execution_time=30  # Timeout in seconds
    )
    
    result = agent_executor.invoke({"input": "Multiply 5 by 3, then add 10"})
    print(f"\nResult: {result['output']}\n")

def example_custom_prompt_agent():
    """Example creating agent with custom prompt"""
    print("=" * 60)
    print("Example 2: Custom Prompt Agent")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @Tool
    def get_info(topic: str) -> str:
        """Get information about a topic."""
        info = {
            "python": "Python is a programming language",
            "ai": "AI stands for Artificial Intelligence",
            "langchain": "LangChain is a framework for LLM applications"
        }
        return info.get(topic.lower(), f"No information about {topic}")
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [get_info]
    
    # Custom prompt template
    prompt = PromptTemplate.from_template("""
    You are a helpful assistant. Use the following tools to answer questions.
    
    Tools: {tools}
    Tool Names: {tool_names}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Question: {input}
    Thought: {agent_scratchpad}
    """)
    
    # Create agent with custom prompt
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    result = agent_executor.invoke({"input": "Tell me about Python"})
    print(f"\nResult: {result['output']}\n")

def example_agent_with_callbacks():
    """Example agent with callbacks"""
    print("=" * 60)
    print("Example 3: Agent with Callbacks")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    from langchain.callbacks import StdOutCallbackHandler
    
    @Tool
    def calculate(expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            result = eval(expression)
            return str(result)
        except:
            return "Error: Invalid expression"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [calculate]
    
    # Create callback handler
    callback = StdOutCallbackHandler()
    
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        callbacks=[callback]
    )
    
    result = agent_executor.invoke({"input": "What is 2 + 2 * 3?"})
    print(f"\nResult: {result['output']}\n")

def example_agent_error_handling():
    """Example advanced error handling"""
    print("=" * 60)
    print("Example 4: Advanced Error Handling")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @Tool
    def risky_operation(value: int) -> str:
        """Perform a risky operation that might fail."""
        if value < 0:
            raise ValueError("Value must be positive")
        return f"Success: processed {value}"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [risky_operation]
    
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True  # Get intermediate steps
    )
    
    # This should handle the error gracefully
    result = agent_executor.invoke({"input": "Process the value -5"})
    print(f"\nResult: {result['output']}\n")
    print(f"Intermediate steps: {len(result.get('intermediate_steps', []))} steps\n")

def example_agent_iteration_limit():
    """Example limiting agent iterations"""
    print("=" * 60)
    print("Example 5: Limiting Agent Iterations")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @Tool
    def simple_task(task: str) -> str:
        """Perform a simple task."""
        return f"Completed: {task}"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [simple_task]
    
    # Limit to 2 iterations
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=2,  # Stop after 2 iterations
        early_stopping_method="force"  # Force stop when limit reached
    )
    
    result = agent_executor.invoke({"input": "Do something simple"})
    print(f"\nResult: {result['output']}\n")

def example_agent_debugging():
    """Example debugging agent execution"""
    print("=" * 60)
    print("Example 6: Debugging Agent Execution")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @Tool
    def debug_tool(input: str) -> str:
        """A tool for debugging."""
        print(f"[DEBUG] Tool called with: {input}")
        return f"Processed: {input}"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    tools = [debug_tool]
    
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,  # Shows detailed execution
        return_intermediate_steps=True
    )
    
    result = agent_executor.invoke({"input": "Debug something"})
    
    print(f"\nFinal Output: {result['output']}")
    print(f"\nIntermediate Steps: {len(result.get('intermediate_steps', []))}")
    for i, step in enumerate(result.get('intermediate_steps', []), 1):
        print(f"  Step {i}: {step[0].tool} -> {step[0].tool_input}")
    print()

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Advanced Agent Execution")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_agent_executor()
        example_custom_prompt_agent()
        example_agent_with_callbacks()
        example_agent_error_handling()
        example_agent_iteration_limit()
        example_agent_debugging()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - AgentExecutor controls agent execution")
        print("  - Custom prompts customize agent behavior")
        print("  - Callbacks allow monitoring agent actions")
        print("  - Error handling prevents crashes")
        print("  - Limit iterations to prevent infinite loops")
        print("  - verbose=True and return_intermediate_steps help debugging\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

