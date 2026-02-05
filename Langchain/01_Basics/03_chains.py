"""
Module 1: Basics - Creating and Using Chains

Chains are sequences of calls to LLMs or other utilities.
This module covers:
1. Simple chains (LLM + Prompt)
2. Sequential chains
3. Router chains
4. Custom chains
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from dotenv import load_dotenv
import os

load_dotenv()

def example_simple_chain():
    """Example of a simple LLMChain"""
    print("=" * 60)
    print("Example 1: Simple Chain (LLM + Prompt)")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        "Explain {topic} in simple terms."
    )
    
    # Create a chain that combines prompt and LLM
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run the chain
    response = chain.invoke({"topic": "blockchain"})
    
    print(f"\nTopic: blockchain")
    print(f"Response: {response['text'][:200]}...\n")

def example_sequential_chain():
    """Example of SimpleSequentialChain (one output feeds into next)"""
    print("=" * 60)
    print("Example 2: Sequential Chain")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # First chain: Generate a story
    story_prompt = ChatPromptTemplate.from_template(
        "Write a short story about {topic}."
    )
    story_chain = LLMChain(llm=llm, prompt=story_prompt, output_key="story")
    
    # Second chain: Summarize the story
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize the following story in one sentence: {story}"
    )
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")
    
    # Combine chains sequentially
    # The output of story_chain becomes input to summary_chain
    sequential_chain = SequentialChain(
        chains=[story_chain, summary_chain],
        input_variables=["topic"],
        output_variables=["story", "summary"],
        verbose=True  # Shows intermediate steps
    )
    
    result = sequential_chain.invoke({"topic": "a robot learning to paint"})
    
    print(f"\nTopic: {result['topic']}")
    print(f"\nStory:\n{result['story']}")
    print(f"\nSummary: {result['summary']}\n")

def example_simple_sequential_chain():
    """Example of SimpleSequentialChain (simpler, one variable passed)"""
    print("=" * 60)
    print("Example 3: Simple Sequential Chain")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Chain 1: Generate a concept
    chain1 = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template("What is {topic}?")
    )
    
    # Chain 2: Explain it simply
    chain2 = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            "Explain the following in simple terms: {input}"
        )
    )
    
    # SimpleSequentialChain automatically passes output of chain1 to chain2
    overall_chain = SimpleSequentialChain(
        chains=[chain1, chain2],
        verbose=True
    )
    
    result = overall_chain.invoke("quantum entanglement")
    print(f"\nFinal Result: {result['output']}\n")

def example_chain_with_formatting():
    """Example showing how to format chain outputs"""
    print("=" * 60)
    print("Example 4: Chain with Custom Formatting")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create a chain that formats output
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that formats information clearly."),
        ("human", """
        Topic: {topic}
        Format: {format}
        
        Provide information about the topic in the requested format.
        """)
    ])
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.invoke({
        "topic": "Python programming",
        "format": "bullet points"
    })
    
    print(f"\nTopic: Python programming")
    print(f"Format: bullet points")
    print(f"\nResponse:\n{result['text']}\n")

def example_chain_batch():
    """Example of running a chain on multiple inputs"""
    print("=" * 60)
    print("Example 5: Running Chain on Multiple Inputs")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_template(
        "Explain {concept} in one sentence."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Process multiple inputs at once
    concepts = ["machine learning", "neural networks", "deep learning"]
    results = chain.batch([{"concept": c} for c in concepts])
    
    print("\nProcessing multiple concepts:\n")
    for concept, result in zip(concepts, results):
        print(f"{concept}: {result['text']}\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN BASICS: Chains")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_simple_chain()
        example_sequential_chain()
        example_simple_sequential_chain()
        example_chain_with_formatting()
        example_chain_batch()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Chains combine prompts and LLMs")
        print("  - Sequential chains pass output from one to the next")
        print("  - Chains can process multiple inputs efficiently")
        print("  - Use verbose=True to see intermediate steps\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

