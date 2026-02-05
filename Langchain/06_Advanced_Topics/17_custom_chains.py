"""
Module 6: Advanced Topics - Building Custom Chains

This module covers:
1. What are custom chains
2. Creating custom chains
3. Chain composition
4. Advanced chain patterns
5. Chain validation
"""

from langchain_openai import ChatOpenAI
from langchain.chains.base import Chain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from typing import Dict, List, Any
from dotenv import load_dotenv
import os

load_dotenv()

class CustomChain(Chain):
    """Example custom chain"""
    prompt: ChatPromptTemplate
    llm: ChatOpenAI
    
    @property
    def input_keys(self) -> List[str]:
        """Define input keys"""
        return ["topic", "audience"]
    
    @property
    def output_keys(self) -> List[str]:
        """Define output keys"""
        return ["explanation"]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the chain"""
        # Format prompt
        messages = self.prompt.format_messages(
            topic=inputs["topic"],
            audience=inputs["audience"]
        )
        
        # Call LLM
        response = self.llm.invoke(messages)
        
        # Return output
        return {"explanation": response.content}

def example_simple_custom_chain():
    """Example of a simple custom chain"""
    print("=" * 60)
    print("Example 1: Simple Custom Chain")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    # Create custom chain
    prompt = ChatPromptTemplate.from_template(
        "Explain {topic} to a {audience}."
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    chain = CustomChain(prompt=prompt, llm=llm)
    
    # Use the chain
    result = chain.invoke({
        "topic": "quantum computing",
        "audience": "5-year-old child"
    })
    
    print(f"\nResult: {result['explanation'][:200]}...\n")

def example_chain_composition():
    """Example composing multiple chains"""
    print("=" * 60)
    print("Example 2: Chain Composition")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    from langchain.chains import LLMChain, SimpleSequentialChain
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Chain 1: Generate idea
    idea_prompt = ChatPromptTemplate.from_template(
        "Generate a creative idea about {topic}"
    )
    idea_chain = LLMChain(llm=llm, prompt=idea_prompt)
    
    # Chain 2: Expand idea
    expand_prompt = ChatPromptTemplate.from_template(
        "Expand on this idea: {input}"
    )
    expand_chain = LLMChain(llm=llm, prompt=expand_prompt)
    
    # Compose chains
    composed_chain = SimpleSequentialChain(
        chains=[idea_chain, expand_chain],
        verbose=True
    )
    
    result = composed_chain.invoke("artificial intelligence")
    print(f"\nFinal result: {result['output'][:200]}...\n")

def example_conditional_chain():
    """Example chain with conditional logic"""
    print("=" * 60)
    print("Example 3: Conditional Chain")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class ConditionalChain(Chain):
        """Chain that routes based on input"""
        llm: ChatOpenAI
        
        @property
        def input_keys(self) -> List[str]:
            return ["query", "type"]
        
        @property
        def output_keys(self) -> List[str]:
            return ["response"]
        
        def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            query = inputs["query"]
            query_type = inputs["type"]
            
            if query_type == "technical":
                prompt = f"Provide a technical explanation: {query}"
            elif query_type == "simple":
                prompt = f"Explain in simple terms: {query}"
            else:
                prompt = f"Answer: {query}"
            
            response = self.llm.invoke(prompt)
            return {"response": response.content}
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    chain = ConditionalChain(llm=llm)
    
    result = chain.invoke({
        "query": "What is machine learning?",
        "type": "simple"
    })
    
    print(f"\nResult: {result['response'][:200]}...\n")

def example_chain_with_validation():
    """Example chain with input validation"""
    print("=" * 60)
    print("Example 4: Chain with Validation")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    class ValidatedChain(Chain):
        """Chain with input validation"""
        llm: ChatOpenAI
        
        @property
        def input_keys(self) -> List[str]:
            return ["text", "max_length"]
        
        @property
        def output_keys(self) -> List[str]:
            return ["summary"]
        
        def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            # Validate inputs
            text = inputs["text"]
            max_length = inputs.get("max_length", 100)
            
            if not text:
                raise ValueError("Text cannot be empty")
            
            if max_length < 10:
                raise ValueError("Max length must be at least 10")
            
            # Process
            prompt = f"Summarize this in {max_length} words or less: {text}"
            response = self.llm.invoke(prompt)
            
            return {"summary": response.content}
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    chain = ValidatedChain(llm=llm)
    
    result = chain.invoke({
        "text": "LangChain is a framework for building LLM applications. It provides tools for chains, agents, and more.",
        "max_length": 20
    })
    
    print(f"\nSummary: {result['summary']}\n")

def example_chain_with_memory():
    """Example custom chain with memory"""
    print("=" * 60)
    print("Example 5: Chain with Memory")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    from langchain.memory import ConversationBufferMemory
    
    class MemoryChain(Chain):
        """Chain with conversation memory"""
        llm: ChatOpenAI
        memory: ConversationBufferMemory
        
        @property
        def input_keys(self) -> List[str]:
            return ["input"]
        
        @property
        def output_keys(self) -> List[str]:
            return ["output"]
        
        def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            # Get memory
            history = self.memory.chat_memory.messages
            
            # Build prompt with history
            prompt = "Previous conversation:\n"
            for msg in history[-4:]:  # Last 4 messages
                prompt += f"{msg.content}\n"
            
            prompt += f"\nCurrent input: {inputs['input']}\nResponse:"
            
            # Call LLM
            response = self.llm.invoke(prompt)
            
            # Save to memory
            self.memory.save_context(
                {"input": inputs["input"]},
                {"output": response.content}
            )
            
            return {"output": response.content}
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    chain = MemoryChain(llm=llm, memory=memory)
    
    # Multi-turn conversation
    result1 = chain.invoke({"input": "My name is Bob"})
    print(f"Turn 1: {result1['output'][:100]}...\n")
    
    result2 = chain.invoke({"input": "What's my name?"})
    print(f"Turn 2: {result2['output']}\n")

def example_chain_pipeline():
    """Example complex chain pipeline"""
    print("=" * 60)
    print("Example 6: Chain Pipeline")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not found. Skipping this example.\n")
        return
    
    from langchain.chains import LLMChain
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Step 1: Generate question
    question_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template("Generate a question about {topic}")
    )
    
    # Step 2: Answer question
    answer_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template("Answer this question: {question}")
    )
    
    # Step 3: Format answer
    format_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template("Format this answer nicely: {answer}")
    )
    
    # Run pipeline
    topic = "Python programming"
    question_result = question_chain.invoke({"topic": topic})
    question = question_result["text"]
    
    answer_result = answer_chain.invoke({"question": question})
    answer = answer_result["text"]
    
    format_result = format_chain.invoke({"answer": answer})
    
    print(f"\nTopic: {topic}")
    print(f"Question: {question}")
    print(f"Answer: {answer[:150]}...")
    print(f"Formatted: {format_result['text'][:150]}...\n")

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN: Custom Chains")
    print("=" * 60 + "\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    try:
        example_simple_custom_chain()
        example_chain_composition()
        example_conditional_chain()
        example_chain_with_validation()
        example_chain_with_memory()
        example_chain_pipeline()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - Custom chains extend LangChain functionality")
        print("  - Chains can be composed for complex workflows")
        print("  - Add validation and error handling")
        print("  - Memory can be integrated into custom chains")
        print("  - Chains enable reusable, testable components\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

