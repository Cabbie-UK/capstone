import streamlit as st
from streamlit_mermaid import st_mermaid

def display_tax_relief_flowchart():
    st.header("Tax Relief Advisor Flow Chart")
    tax_relief_chart = """
    flowchart TD
        Start[Start] --> Form[Display Tax Relief Form]
        Form --> InputFields[Collect User Inputs]
        InputFields --> |Input Fields| Details[["
            - Citizenship
            - Gender
            - Marital Status
            - Children
            - Employment Status"]]
        
        InputFields --> Submit{Submit Form?}
        Submit -->|No| InputFields
        Submit -->|Yes| ProcessInputs[Process User Inputs]
        
        ProcessInputs --> FilterReliefs[Filter Eligible Tax Reliefs]
        FilterReliefs --> DisplayReliefs[Display Eligible Reliefs]
        
        DisplayReliefs --> ChatInterface[Show Chat Interface]
        ChatInterface --> UserQuery{User Query?}
        
        UserQuery -->|Yes| ProcessQuery[Process Query with LLM]
        ProcessQuery --> RetrieveInfo[Retrieve Relevant Information]
        RetrieveInfo --> GenerateResponse[Generate Response]
        GenerateResponse --> DisplayResponse[Display Response]
        DisplayResponse --> UserQuery
        
        UserQuery -->|Clear Chat| ResetChat[Reset Chat History]
        ResetChat --> ChatInterface
        
        UserQuery -->|No| End[End]

        style Start fill:#90EE90
        style End fill:#FFB6C1
    """
    st_mermaid(tax_relief_chart)

def display_rental_income_flowchart():
    st.header("Rental Income Calculator Flow Chart")
    rental_income_chart = """
    flowchart TD
        Start[Start] --> PropertyInput[Input Property Details]
        PropertyInput --> InputFields[["Collect for each property:
            - Rental Income
            - Co-ownership Status
            - Ownership Share
            - Expenses"]]
        
        InputFields --> InitSetup[Initialise Analysis Components]
        InitSetup --> VectorStore[Initialise Vector Store]
        VectorStore --> QAChain[Create QA Chain]
        
        QAChain --> FetchGuidelines[Fetch Tax Guidelines]
        FetchGuidelines --> Guidelines1[Tax Deduction Guidelines]
        FetchGuidelines --> Guidelines2[Computation Guidelines]
        FetchGuidelines --> Guidelines3[Strategy Guidelines]
        
        Guidelines1 & Guidelines2 & Guidelines3 --> CreateChains[Create LangChain Components]
        
        CreateChains --> TaxSpecialist[Tax Specialist Chain]
        TaxSpecialist --> |Analyse Expenses| ExpenseAnalysis[["For each property:
            - Review expense categories
            - Check tax deductibility
            - Perform tax research if needed
            - Categorise expenses
            - Apply ownership share"]]
        
        ExpenseAnalysis --> RentComputation[Rent Computation Chain]
        RentComputation --> |Calculate Methods| Methods[["Calculate using:
            1. Actual Expense Method:
                - Subtract allowable expenses
                - Apply ownership share
            2. Simplified Method:
                - Deduct mortgage interest
                - Apply 15% deemed expenses
                - Apply ownership share"]]
        
        Methods --> Strategist[Strategist Chain]
        Strategist --> Report[["Generate Final Report:
            - Per-property breakdown
            - Method comparison
            - Recommended method
            - Compliance reminders"]]
        
        Report --> End[End]

        style Start fill:#90EE90
        style End fill:#FFB6C1
    """
    st_mermaid(rental_income_chart)

def display_flowcharts():
    display_tax_relief_flowchart()
    display_rental_income_flowchart()