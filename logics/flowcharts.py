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
        Start[Start] --> Step1[Step 1: Enter Property Details]
        
        Step1 --> NumProperties[Input Number of Properties]
        NumProperties --> PropertyLoop[["For each property:
            - Rental Income
            - Co-ownership Status
            - Ownership Share
            - Expenses"]]
        
        PropertyLoop --> ExpenseDetails[["Add Expenses:
            - Category
            - Amount
            - Description"]]
        
        ExpenseDetails --> Step2[Step 2: Review Details]
        Step2 --> Modify{Modify Details?}
        Modify -->|Yes| Step1
        
        Modify -->|No| Step3[Step 3: Generate Report]
        Step3 --> InitiateAnalysis[Start CrewAI Analysis]
        
        InitiateAnalysis --> TaxSpecialist[Tax Deduction Specialist Analysis]
        TaxSpecialist --> |Analyse Expenses| AllowableExp[["Determine:
            - Allowable Expenses
            - Non-allowable Expenses
            - Justifications"]]
        
        AllowableExp --> RentExpert[Rent Computation Expert Analysis]
        RentExpert --> |Calculate| TwoMethods[["Calculate using:
            1. Actual Expense Method
            2. Simplified Method (15%)"]]
        
        TwoMethods --> Strategist[Rental Income Strategist Analysis]
        Strategist --> CompareResults[Compare Both Methods]
        CompareResults --> GenerateReport[Generate Final Report]
        
        GenerateReport --> DisplayResults[Display Analysis Results]
        DisplayResults --> End[End]

        style Start fill:#90EE90
        style End fill:#FFB6C1
    """
    st_mermaid(rental_income_chart)

def display_flowcharts():
    display_tax_relief_flowchart()
    display_rental_income_flowchart()