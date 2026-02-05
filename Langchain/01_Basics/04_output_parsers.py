"""
Module 1: Basics - Parsing LLM Outputs

This module teaches you how to:
1. Parse structured outputs from LLMs
2. Use Pydantic models for validation
3. Handle parsing errors
4. Extract specific information from responses
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

# Define Pydantic models for structured output
class Person(BaseModel):
    """Information about a person"""
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age")
    occupation: str = Field(description="The person's job or role")
    hobbies: List[str] = Field(description="List of hobbies")

class Recipe(BaseModel):
    """Recipe information"""
    name: str = Field(description="Name of the recipe")
    ingredients: List[str] = Field(description="List of ingredients")
    steps: List[str] = Field(description="Cooking steps")
    prep_time: int = Field(description="Preparation time in minutes")

def example_pydantic_parser():
    """Example using PydanticOutputParser"""
    print("=" * 60)
    print("Example 1: Pydantic Output Parser")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create a parser for the Person model
    parser = PydanticOutputParser(pydantic_object=Person)
    
    # Create a prompt that includes format instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. {format_instructions}"),
        ("human", "Tell me about a fictional person named Alex.")
    ])
    
    # Format the prompt with parser instructions
    formatted_prompt = prompt.format_messages(
        format_instructions=parser.get_format_instructions()
    )
    
    response = llm.invoke(formatted_prompt)
    
    # Parse the output
    parsed_output = parser.parse(response.content)
    
    print(f"\nRaw Response:\n{response.content[:200]}...\n")
    print(f"Parsed Output:")
    print(f"  Name: {parsed_output.name}")
    print(f"  Age: {parsed_output.age}")
    print(f"  Occupation: {parsed_output.occupation}")
    print(f"  Hobbies: {', '.join(parsed_output.hobbies)}\n")

def example_list_parser():
    """Example using CommaSeparatedListOutputParser"""
    print("=" * 60)
    print("Example 2: List Output Parser")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Parser for comma-separated lists
    parser = CommaSeparatedListOutputParser()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. {format_instructions}"),
        ("human", "List 5 programming languages.")
    ])
    
    formatted_prompt = prompt.format_messages(
        format_instructions=parser.get_format_instructions()
    )
    
    response = llm.invoke(formatted_prompt)
    parsed_list = parser.parse(response.content)
    
    print(f"\nRaw Response: {response.content}")
    print(f"\nParsed List:")
    for i, item in enumerate(parsed_list, 1):
        print(f"  {i}. {item}")
    print()

def example_structured_parser():
    """Example using StructuredOutputParser with ResponseSchema"""
    print("=" * 60)
    print("Example 3: Structured Output Parser")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Define response schemas
    response_schemas = [
        ResponseSchema(name="title", description="Title of the book"),
        ResponseSchema(name="author", description="Author of the book"),
        ResponseSchema(name="genre", description="Genre of the book"),
        ResponseSchema(name="year", description="Publication year"),
    ]
    
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a book expert. {format_instructions}"),
        ("human", "Tell me about a famous science fiction book.")
    ])
    
    formatted_prompt = prompt.format_messages(
        format_instructions=parser.get_format_instructions()
    )
    
    response = llm.invoke(formatted_prompt)
    parsed_output = parser.parse(response.content)
    
    print(f"\nRaw Response:\n{response.content[:200]}...\n")
    print(f"Parsed Output:")
    for key, value in parsed_output.items():
        print(f"  {key}: {value}")
    print()

def example_recipe_parser():
    """Example parsing a recipe with Pydantic"""
    print("=" * 60)
    print("Example 4: Recipe Parser (Complex Pydantic Model)")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=Recipe)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a chef. {format_instructions}"),
        ("human", "Create a recipe for {dish}.")
    ])
    
    formatted_prompt = prompt.format_messages(
        format_instructions=parser.get_format_instructions(),
        dish="chocolate chip cookies"
    )
    
    response = llm.invoke(formatted_prompt)
    recipe = parser.parse(response.content)
    
    print(f"\nRecipe: {recipe.name}")
    print(f"\nPrep Time: {recipe.prep_time} minutes")
    print(f"\nIngredients:")
    for ingredient in recipe.ingredients:
        print(f"  - {ingredient}")
    print(f"\nSteps:")
    for i, step in enumerate(recipe.steps, 1):
        print(f"  {i}. {step}")
    print()

def example_error_handling():
    """Example showing error handling in parsing"""
    print("=" * 60)
    print("Example 5: Error Handling in Parsing")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=Person)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. {format_instructions}"),
        ("human", "Tell me about someone.")
    ])
    
    formatted_prompt = prompt.format_messages(
        format_instructions=parser.get_format_instructions()
    )
    
    response = llm.invoke(formatted_prompt)
    
    # Try to parse with error handling
    try:
        parsed_output = parser.parse(response.content)
        print(f"✅ Successfully parsed:")
        print(f"  Name: {parsed_output.name}")
        print(f"  Age: {parsed_output.age}\n")
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        print(f"\nRaw response: {response.content[:200]}...\n")
        
        # You can use parse_with_prompt for better error recovery
        try:
            parsed_output = parser.parse_with_prompt(response.content, formatted_prompt)
            print(f"✅ Recovered with parse_with_prompt:")
            print(f"  Name: {parsed_output.name}\n")
        except Exception as e2:
            print(f"❌ Recovery also failed: {e2}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN BASICS: Output Parsers")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_pydantic_parser()
        example_list_parser()
        example_structured_parser()
        example_recipe_parser()
        example_error_handling()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Output parsers structure LLM responses")
        print("  - Pydantic models provide type safety")
        print("  - Parsers can handle lists, dicts, and complex objects")
        print("  - Always handle parsing errors gracefully\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

