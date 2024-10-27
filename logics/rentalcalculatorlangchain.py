__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# langchain_rental.py
from typing import List, Dict
import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import SequentialChain, LLMChain
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv

load_dotenv('.env')

def perform_tax_research(query: str) -> dict:
    """
    Perform a Google search using SerpAPI for tax-related queries
    
    Args:
        query: Search query string
        
    Returns:
        dict: Relevant search results
    """
    search_params = {
        "q": f"Singapore tax deductibility {query} rental property",
        "hl": "en",
        "gl": "sg",
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    
    search = GoogleSearch(search_params)
    results = search.get_dict()
    
    # Extract organic results
    if "organic_results" in results:
        return {
            "title": results["organic_results"][0]["title"] if results["organic_results"] else "",
            "snippet": results["organic_results"][0]["snippet"] if results["organic_results"] else "",
            "link": results["organic_results"][0]["link"] if results["organic_results"] else ""
        }
    return {"title": "", "snippet": "", "link": ""}

def initialise_vector_store():
    """Initialize and return the Chroma vector store"""
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
    vector_store = Chroma(
        collection_name="rental_info",
        embedding_function=embeddings_model,
        persist_directory="./chroma_langchain_db"
    )
    return vector_store

def create_qa_chain(vector_store):
    """Create a retrieval QA chain for tax-related queries"""
    llm = ChatOpenAI(temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(k=5),
        return_source_documents=True
    )

def get_tax_guidelines(qa_chain, query: str) -> str:
    """Query the vector store for tax-related information"""
    result = qa_chain.invoke({"query": query})
    return result["result"]

def create_tax_specialist_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["properties_list", "tax_guidelines"],
        template="""You are a Tax Deduction Specialist analyzing rental information for tax deduction purposes.

Tax Guidelines Reference:
{tax_guidelines}

Properties Data: {properties_list}

Using the provided tax guidelines and property data, analyse each property to determine allowable expenses:

For each property:
1. Review all expense categories and descriptions
2. Using the tax guidelines provided, determine if each expense qualifies as tax-deductible
3. For any expense where tax deductibility is unclear:
   - Call the perform_tax_research() function with the expense item as the query
   - Example: research_results = perform_tax_research("property management fees")
   - Incorporate the search results into your decision
4. Categorise expenses as allowable or non-allowable
5. Provide brief explanations for non-allowable expenses, citing relevant guidelines or search results
6. If co-ownership status is 'False', co-ownership share is 100%.

Please format your response as a structured analysis of each property, including:
- Property number
- Rental income
- Co-ownership status and share
- For each expense:
  - Category
  - Amount
  - Description
  - Tax deductibility status
  - Explanation if not allowable, with reference to specific guidelines or search results

Focus on clear, factual determinations based on the provided Singapore tax regulations and verified information.""")

def create_rent_computation_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["tax_specialist_output", "computation_guidelines"],
        template="""You are a Rent Computation Expert calculating taxable rental income using two methods.

Tax Computation Guidelines:
{computation_guidelines}

Previous Analysis: {tax_specialist_output}

Using the provided guidelines, calculate taxable rental income for each property using:

    1. Actual Expense Claims Method:
    - Subtract allowable expenses from gross rental income
    - Apply ownership share to the result. 

    2. Simplified Rental Expense Claims Method:
    - Deduct full mortgage interest from gross rental income
    - Deduct 15 percent of gross rental income as deemed expenses
    - Apply ownership share to the result.

        Example for Simplified Rental Expense Claims Method:
        - Gross Rental Income = $60,000
        - Mortgage Interest = $12,000
        - Deemed Expenses = 15 percent of $60,000 = $9,000
        - Taxable Rent = $60,000 - $12,000 - $9,000 = $39,000

If co-ownership status is 'True:
- Multiply the net rental income or loss by the property ownership percentage to determine the user's taxable rental income or loss.
    Example:
    - Gross Rental Income = $60,000
    - Deductible Expenses = $40,000
    - Property Ownership Share = 20%
    - Taxable Rent: ($60,000 - $40,000) * 20% = $4,000

For each property and method, show:
- Rental Income
- Deductible Expenses (itemized)
- Ownership share
- Taxable Rent calculation
- Non-deductible expenses with explanations

Calculate total taxable rent across all properties for each method.
Handle rental losses by offsetting against other properties' income.
This is applicable to both Actual Expense and Simplified Reatal Expense claims method.
    Example:
    - Taxable Rent from Property A = $30000
    - Taxable Rent from Property B (loss) = (-$10000)
    - Total Taxable Rent from all properties = $30000 + (-$10000) = $20000

""")

def create_strategist_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["computation_results", "strategy_guidelines"],
        template="""You are a Rental Income Strategist providing tax reporting advice.

Tax Strategy Guidelines:
{strategy_guidelines}

Computation Results: {computation_results}

Create a markdown report showing:

1. For each claim method:
   - Per-property breakdown:
     - Rental Income
     - Deductible Expenses
     - Ownership share
     - Taxable Rent
     - Non-deductible expenses with explanations
   - Total taxable rent for all properties. Do NOT combine the Total taxable rent for all properties for both claim methods.

2. Your recommendation:
   - Identify the method that results in lower taxable rent
   - Explain benefits and considerations of the recommended method, referencing the guidelines
   - If both methods yield the same result, explain pros and cons without making a recommendation

3. Important reminders:
   - Owner's responsibility for accurate tax reporting
   - Requirement to keep expense records for 5 years
   - Any specific compliance requirements from the guidelines

Do not use markdown code blocks in your response.""")

def run_rental_analysis(property_list: List[Dict]) -> str:
    """
    Analyze rental properties using LangChain with vector store integration.
    
    Args:
        property_list: List of property dictionaries containing rental information
        
    Returns:
        str: Analysis results in markdown format
    """
    # Initialize vector store and QA chain
    vector_store = initialise_vector_store()
    qa_chain = create_qa_chain(vector_store)

    # Retrieve relevant tax guidelines for each stage
    tax_guidelines = get_tax_guidelines(qa_chain, 
        "What are the allowable and non-allowable rental expenses for tax deduction in Singapore?")
    computation_guidelines = get_tax_guidelines(qa_chain,
        "How to calculate taxable rental income using actual expense claims method and simplified method?")
    strategy_guidelines = get_tax_guidelines(qa_chain,
        "What are the benefits and considerations for choosing between actual expense claims and simplified rental expense claims methods?")

    # Initialize LLM
    llm = ChatOpenAI(temperature=0)
    output_parser = StrOutputParser()

    # Create chains for each analysis step
    tax_specialist_chain = LLMChain(
        llm=llm,
        prompt=create_tax_specialist_prompt(),
        output_key="tax_specialist_output",
        verbose=True
    )

    rent_computation_chain = LLMChain(
        llm=llm,
        prompt=create_rent_computation_prompt(),
        output_key="computation_results",
        verbose=True
    )

    strategist_chain = LLMChain(
        llm=llm,
        prompt=create_strategist_prompt(),
        output_key="final_report",
        verbose=True
    )

    # Combine chains
    analysis_chain = SequentialChain(
        chains=[tax_specialist_chain, rent_computation_chain, strategist_chain],
        input_variables=["properties_list", "tax_guidelines", "computation_guidelines", "strategy_guidelines"],
        output_variables=["final_report"],
        verbose=True
    )

    # Run analysis
    result = analysis_chain.invoke({
        "properties_list": str(property_list),
        "tax_guidelines": tax_guidelines,
        "computation_guidelines": computation_guidelines,
        "strategy_guidelines": strategy_guidelines
    })

    return result["final_report"]