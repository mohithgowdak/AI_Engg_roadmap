"""
Module 5: Agents - Creating Custom Tools

This module covers:
1. What are tools
2. Creating custom tools
3. Tool decorators
4. Complex tools
5. Tool descriptions
"""

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

def example_simple_tool():
    """Example creating a simple custom tool"""
    print("=" * 60)
    print("Example 1: Simple Custom Tool")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Define a simple tool function
    def get_word_length(word: str) -> str:
        """Returns the length of a word."""
        return str(len(word))
    
    # Create Tool object
    word_length_tool = Tool(
        name="WordLength",
        func=get_word_length,
        description="Useful when you need to find the length of a word. Input should be a single word."
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[word_length_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    result = agent.invoke("What is the length of the word 'LangChain'?")
    print(f"\nResult: {result['output']}\n")

def example_tool_decorator():
    """Example using @tool decorator"""
    print("=" * 60)
    print("Example 2: Tool Decorator")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Using @tool decorator (simpler way)
    @tool
    def calculate_area(length: float, width: float) -> float:
        """Calculate the area of a rectangle.
        
        Args:
            length: The length of the rectangle
            width: The width of the rectangle
            
        Returns:
            The area of the rectangle
        """
        return length * width
    
    @tool
    def get_current_time() -> str:
        """Get the current date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[calculate_area, get_current_time],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    result = agent.invoke("What is the area of a rectangle with length 5 and width 3?")
    print(f"\nResult: {result['output']}\n")

def example_tool_with_pydantic():
    """Example tool with Pydantic schema"""
    print("=" * 60)
    print("Example 3: Tool with Pydantic Schema")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Define input schema
    class CalculatorInput(BaseModel):
        """Input for calculator tool."""
        a: float = Field(description="First number")
        b: float = Field(description="Second number")
        operation: str = Field(description="Operation: add, subtract, multiply, or divide")
    
    @tool(args_schema=CalculatorInput)
    def calculator(a: float, b: float, operation: str) -> float:
        """Perform basic arithmetic operations."""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero"
            return a / b
        else:
            return "Error: Invalid operation"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[calculator],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    result = agent.invoke("Multiply 15 by 8")
    print(f"\nResult: {result['output']}\n")

def example_multiple_tools():
    """Example agent with multiple custom tools"""
    print("=" * 60)
    print("Example 4: Multiple Custom Tools")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @tool
    def reverse_string(text: str) -> str:
        """Reverse a string."""
        return text[::-1]
    
    @tool
    def uppercase_string(text: str) -> str:
        """Convert a string to uppercase."""
        return text.upper()
    
    @tool
    def count_words(text: str) -> int:
        """Count the number of words in a string."""
        return len(text.split())
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[reverse_string, uppercase_string, count_words],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    result = agent.invoke("Reverse the string 'Hello World' and count its words")
    print(f"\nResult: {result['output']}\n")

def example_tool_with_error_handling():
    """Example tool with error handling"""
    print("=" * 60)
    print("Example 5: Tool with Error Handling")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    @tool
    def divide_numbers(a: float, b: float) -> str:
        """Divide two numbers. Handles division by zero."""
        try:
            if b == 0:
                return "Error: Cannot divide by zero"
            result = a / b
            return f"The result is {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @tool
    def get_weather(city: str) -> str:
        """Get weather information for a city. (Mock implementation)"""
        # In real implementation, this would call a weather API
        weather_data = {
            "New York": "Sunny, 72°F",
            "London": "Cloudy, 60°F",
            "Tokyo": "Rainy, 68°F"
        }
        return weather_data.get(city, f"Weather data not available for {city}")
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[divide_numbers, get_weather],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Test error handling
    result1 = agent.invoke("What is 10 divided by 0?")
    print(f"\nResult 1: {result1['output']}\n")
    
    # Test normal operation
    result2 = agent.invoke("What's the weather in New York?")
    print(f"Result 2: {result2['output']}\n")

def example_tool_descriptions():
    """Example showing importance of good tool descriptions"""
    print("=" * 60)
    print("Example 6: Tool Descriptions Matter")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Good description helps agent understand when to use the tool
    @tool
    def search_database(query: str) -> str:
        """Search the company database for information.
        
        Use this tool when you need to find information stored in the database.
        The query should be a search term or question.
        
        Args:
            query: The search query or question
            
        Returns:
            Relevant information from the database
        """
        # Mock database search
        mock_db = {
            "employee count": "We have 150 employees",
            "revenue": "Annual revenue is $10 million",
            "products": "We sell software products"
        }
        
        # Simple keyword matching (in real app, use proper search)
        for key, value in mock_db.items():
            if key in query.lower():
                return value
        return "No information found in database"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    agent = initialize_agent(
        tools=[search_database],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    result = agent.invoke("How many employees does the company have?")
    print(f"\nResult: {result['output']}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Custom Agent Tools")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_simple_tool()
        example_tool_decorator()
        example_tool_with_pydantic()
        example_multiple_tools()
        example_tool_with_error_handling()
        example_tool_descriptions()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Tools extend agent capabilities")
        print("  - @tool decorator simplifies tool creation")
        print("  - Pydantic schemas provide type safety")
        print("  - Good descriptions help agents use tools correctly")
        print("  - Always handle errors in tools\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

