__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# modules/crew_analysis.py
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool
from helper_functions.tools import search_rental_info, serpapi_search, read_json_file

load_dotenv('.env')

def create_agents():
    web_rag_tool = WebsiteSearchTool()

    tax_deduction_specialist = Agent(
        role="Tax Deduction Specialist",
        goal="Determine if expenses claimed against rental income are allowable for tax purposes.",
        backstory="""
        For tax purposes, only expenses incurred exclusively for producing rental income are tax-deductible. 
        As a Tax Deduction Specialist, your expertise, aided by reference materials, will be critical in identifying which expenses qualify under this rule.
        """,
        tools=[search_rental_info, serpapi_search, web_rag_tool],
        allow_delegation=False,
        verbose=False,
    )

    rent_computation_expert = Agent(
        role="Rent Computation Expert",
        goal="Compute the taxable rent for each property using either the actual expenses claims method or the simplified rental expense claims method.",
        backstory="""Following tax guidelines and reference documents provided, the Rent Computation Expert works with information from the Tax Deduction Specialist to determine taxable rental income, ensuring accuracy across multiple properties.
        The agent is responsible for producing clear, comprehensive results for each method.
        """,
        #tools=[search_rental_info],
        allow_delegation=False,
        verbose=True,
    )

    rental_income_strategist = Agent(
        role="Rental Income Strategist",
        goal="Advise on the method which results in lower rental income reporting.",
        backstory="""Acting as the final decision-making agent, the Rental Income Strategist ensures the user pays lower taxes legitimately by comparing reporting methods. 
        This agent's role is critical in presenting a balanced view, considering both short-term savings and long-term implications.
        """,
        tools=[search_rental_info],
        allow_delegation=False,
        verbose=True,
    )

    return tax_deduction_specialist, rent_computation_expert, rental_income_strategist

def create_tasks(tax_specialist, rent_expert, strategist,properties_list):

    web_rag_tool = WebsiteSearchTool()

    determine_allowable_expenses = Task(
        description=f"""
        Analyze the rental information for tax deduction purposes.
        1. Use the provided properties list data for analysis
        2. Review the provided expense categories and descriptions for each property 
        3. Utilize tax regulations and available reference documents to assess whether each expense qualifies as tax-deductible.
        4. Where the expense description does not clearly fall under allowable rental expenses:
            a. Conduct a search, on the expense description using the serpai_search tool to return the relevant urls about its tax deductibility.
            b. Use the web_rag_tool to research on the returned URLs to ascertain the tax deductibility of the expense under Singapore tax system.
        5. Categorize expenses as either allowable or non-allowable.
        6. Provide a brief explanation for each non-allowable expense.       
        
        Properties data: {properties_list}

        When using search_rental_info or serpapi_search tool, provide a simple text query string, for example:
            search_rental_info("what are allowable rental expenses in Singapore")     
        
        """,
        expected_output="""
        A structured string containing the following info for each reported property:
        - property number, 
        - rental income, 
        - whether property is co-owned, 
        - ownership share, 
        - For each expense:
            - category, 
            - amount
            - description
            - Whether the epxpense is tax deductible,
            - the explanation if it is not an allowable expense.
        
        """,
        tools=[serpapi_search, web_rag_tool],
        agent=tax_specialist,
        async_execution=True
    )

    compute_rent = Task(
        description=f"""
        1. Gather data from the Tax Deduction Specialist on allowable expenses.
        2. Calculate the Singapore taxable rental income for each property under the following methods:
            A. Actual Expense Claims Method: 
            - Subtract all allowable expenses from the gross rental income.
            - The result is the taxable rental income or loss.

                Steps:
                a. Determine the gross rental income.
                b. Identify and sum up all allowable expenses (e.g., repairs, maintenance, insurance).
                c. Subtract the total allowable expenses from the gross rental income to calculate the taxable rent.

            B. Simplified Rental Expense Claims Method: 
            - Apply the 15% deemed rental expense method.
            - Deduct the full amount of mortgage interest incurred from purchasing the property.
            - Additionally, deduct 15% of the gross rental income as deemed expenses.

                Steps:
                a. Determine the gross rental income.
                b. Deduct the mortgage interest amount from the gross rental income.
                c. Calculate 15% of the gross rental income and deduct this amount as deemed expenses.
                d. Subtract both the mortgage interest and deemed expenses from the gross rental income to determine the taxable rent.

                Example for Simplified Method:
                - Gross Rental Income = $60,000
                - Mortgage Interest = $12,000
                - Deemed Expenses = 15% of $60,000 = $9,000
                - Taxable Rent = $60,000 - $12,000 - $9,000 = $39,000

        3. Calculate the taxable rental income or loss by applying the property ownership share. 
            This is applicable for both claims methods.
            Steps:
            a. Determine the gross rental income.
            b. Subtract deductible expenses from the gross rental income to get the net rental income or loss.
            c. Multiply the net rental income or loss by the property ownership percentage to determine the user's taxable rental income or loss.

                Example:
                - Gross Rental Income = $60,000
                - Deductible Expenses = $40,000
                - Property Ownership Share = 20%
                - Taxable Rent: ($60,000 - $40,000) * 20% = $4,000

        4. Rental loss of one property to offset against the taxable rental income of another property.
            This is applicable to both claims methods.
                Example:
                - Taxable Rent from Property A = $30000
                - Taxable Rent from Property B (loss) = (-$10000)
                - Total Taxable Rent from all properties = $30000 + (-$10000) = $20000
 
        """,
        expected_output="""
        A structured string containing the following info:
        - Under each claim method:
            - For each property:
                - Rental Income
                - Deductible Expenses
                - Ownership share of property (if is_co_owned is False, then this is 100%)
                - Taxable Rent
                - Expenses that are not deductible and explanation
                
        - Total taxable rent for all properties 
        """,
        agent=rent_expert,
        async_execution=False,
        context=[determine_allowable_expenses]
    )

    advise_tax_reporting = Task(
        description="""
        1. Analyse the outputs provided by the rent_computation_expert
        2. Recommend the method which results in lower taxabale rent, explaining both the benefits and points to note.
        3. When both methods result in the same taxable rent, explain the pros and cons of each claims method without recommendation either method.
        4. Briefly highlight that it's the owner's responsibility to ensure that all tax reporting are done correctly and timely.
        5. When using search_rental_info tool, provide a simple text query string, for example:
           - search_rental_info("What are the benefits and points to note under Simplified Rental Expense Claims Method in Singapore?")            
        
        """,
        expected_output="""
        1. An report, in markdown format, to show the following:
        - Under each claim method:
            -For each property:
                - Rental Income
                - Deductible Expenses
                - Ownership share of property (if co_owned is False, then this 100%)
                - Taxable Rent
                - Expenses that are not deductible and explanation
            - Total taxable rent for all properties.
        - Do NOT combine the Total taxable rent for all properties for both claim methods.
        - Recommend the method which in lower taxabale rent, explaining both the benefits and points to note.
        - Briefly highlight that it's the owner's responsibility to ensure that all tax reporting are done correctly and timely. Owner to keep complete records of expense claims for 5 years.   
        2. Do NOT enclose the output in tripe backticks
        """,
        agent=strategist,
        async_execution=False,
        context=[compute_rent]
    )

    return determine_allowable_expenses, compute_rent, advise_tax_reporting

def run_crew_analysis(properties_list: list):
    """
    Run the CrewAI analysis with the provided properties list.
    
    Args:
        properties_list (list): List containing property data
        
    Returns:
        str: Analysis results in markdown format
    """
    # Create agents
    tax_specialist, rent_expert, strategist = create_agents()
    
    # Create tasks with the provided list
    task1, task2, task3 = create_tasks(
        tax_specialist, 
        rent_expert, 
        strategist, 
        properties_list
    )
    
    # Assemble crew
    crew = Crew(
        agents=[tax_specialist, rent_expert, strategist],
        tasks=[task1, task2, task3],
        verbose=True,
        planning=False,
    )

    # Run the crew
    result = crew.kickoff()

    return result.raw