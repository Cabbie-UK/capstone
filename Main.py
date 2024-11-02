__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from helper_functions.utility import check_password

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    page_title="TaxEase Tax Advisor",
    page_icon="🤖",
    layout="wide"
)

# Check if the password is correct.  
if not check_password():  
    st.stop()

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from logics.datafile import filter_and_get_reliefs, capture_and_store
from helper_functions.llm import get_chatbot_response
import pandas as pd
import requests.exceptions

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #4B0082;
    }
    .highlight {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stNumberInput>div>div>input {
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    .stAlert {
        border-radius: 10px;
    }
    #GithubIcon {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# region <--------- Initialise env variables and load vector store --------->

load_dotenv('.env')

# Load the vector store collection for tax reliefs
# Refer to the generate_chroma_db_for_reliefs.py script at the root folder to create the vector store
# cache this resource for faster loading
@st.cache_resource
def load_vector_store():
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
    vector_store = Chroma(
        collection_name="various_tax_relief",
        embedding_function=embeddings_model,
        persist_directory="./chroma_langchain_db"
    )
    return vector_store      

vector_store = load_vector_store()
retriever = vector_store.as_retriever(k=5)

# region <--------- Setup system message and initialise messages object --------->

# Setup system message for the tax relief chatbot
system_message = """
You are an intelligent assistant specializing in tax relief queries relating to Singapore tax system using the information available in the Chroma database or your own knowledge. 
Your user may use online form to provide some information about himself, and this is captured in the messages object. 
You shall make use of the information availble in your knowledge base to answer the user queries.

If and only if you have absolutely no information to offer, please inform user to send the query to IRAS through the following 
channels:
1. Live Chat: https://go.gov.sg/iras-livechat
2. Call: 1800 356 8300 for local calls or (+65) 6356 8300 from overseas
3. Email: https://mytax.iras.gov.sg/portal/correspondence/mytax-mail
"""

# Always initiate the chatbot with the system message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message}
    ]

# region <--------- Page Title and Header --------->

col1, col2 = st.columns([2, 1])
with col1:
    st.title("🤖 TaxEase: Your Helpful GenAI Tax Advisor")
    st.subheader("Intelligent Tax Advisory Solutions")

# Warning a message, a project requirement
with st.expander('⚠️ Important Information'):
    st.markdown("""
    **IMPORTANT NOTICE**: This web application is a prototype developed for **educational purposes only**. The information provided here is **NOT** intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    **Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

    Always consult with qualified professionals for accurate and personalized advice.
    """)

st.write('Choose one of the two tax matters I can assist you with:')

# Create tabs with improved styling
# Displays the 2 use cases as part of the project requirements
relief, rent = st.tabs([" 💰 Claim Tax Reliefs ", " 🏠 Calculate Taxable Rental Income"])

# region <--------- Use Case 1: Claim Tax Reliefs tab --------->
with relief:
    st.header("Claim Tax Reliefs")
    st.write("""
        Welcome! I'm here to help you discover the tax reliefs you're eligible for, so you can potentially lower your tax payments and save more. 
        
        To get started, tell me a bit about yourself, and I'll narrow down the tax benefits tailored to your situation.                                    
            """)    
    st.warning('You are eligible for personal reliefs and rebates if you are a Singapore Tax Resident and if you fulfilled the qualifying conditions of the reliefs and rebates')
    st.info('Note: Only a tax resident (including non-Singapore Citizens who are in Singapore for more than 183 days in a year) can claim for tax relief.')
    
    with st.form(key="form"):
        st.write("Please select the option that applies to you for the following questions:")

        
        citizenship = st.radio(
                                "Qn 1. Your Citizenship",
                                options = ['Singaporean','Permanent Resident','Foreigner'],
                                index=None,
                                horizontal=True
                                )
        gender = st.radio(
                                "Qn 2. Your Gender",
                                options = ['Male','Female'],
                                index=None,
                                horizontal=True
                                )
        maritial_status = st.radio(
                                "Qn 3. Your Maritial Status",
                                options = ['Single','Married','Divorced'],
                                index=None,
                                horizontal=True
                                )
        children = st.radio(
                            "Qn 4. Do you have children?",
                            options = ['Yes','No'],
                            index=None,
                            horizontal=True
                            )
        employment = st.radio(
                        "Qn 5. Your Employment Status",
                        options = ['Employed (including part-timers)/ Self-employed','Unemployed'],
                        index=None,
                        horizontal=True
                        )               
            
        submit_filter = st.form_submit_button(label="Find Eligible Tax Reliefs" )

    if submit_filter:
        with st.spinner('Finding eligible tax reliefs...'):
            # The capture_and_store function is available in .logics>datafile.py
            # Does not require all 5 profile attributes to be provided
            user_prompt = capture_and_store(citizenship=citizenship, 
                                            gender=gender,
                                            maritial_status=maritial_status,
                                            employment=employment,
                                            children=children)
            
            # Insert this in to the messages object as the user's initial query
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            
            # The filter_and_get_reliefs function is available in .logic>datafile.py
            llm_response = filter_and_get_reliefs(citizenship=citizenship, 
                                            gender=gender,
                                            maritial_status=maritial_status,
                                            employment=employment,
                                            children=children)
            
            # Insert this into the messages object as the assistant's response to user's initial query        
            st.session_state.messages.append({"role": "assistant", "content": llm_response})

# region <--------- Use Case 1: Chat Conversation region --------->
    st.subheader("Chat Conversation")
    # Create chat container 
    chat_container = st.container(height=500, border=True)

    # Create a placeholder for the spinner
    spinner_placeholder = st.empty()

    # Chat input box 
    if prompt := st.chat_input("Ask me anything related to Singapore tax reliefs:"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Show spinner while generating response
        with spinner_placeholder:
            with st.spinner('Thinking...'):
                response = get_chatbot_response(prompt=prompt,
                                          retriever=retriever,
                                          messages=st.session_state.messages) # refer to messages object for earlier conversations
        
        # Clear the spinner placeholder after response is generated
        spinner_placeholder.empty()
        
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display messages in chat container
    with chat_container:
        if len(st.session_state.messages) > 1:
            for message in st.session_state.messages:
                # Omit the display of system message
                if message["role"] != "system":
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
        else:
            # Show a placeholder or initial instruction when no messages exist
            st.info("Your chat history will appear here after you submit the form or start chatting.")

    # Clear chat button 
    if st.button("Clear Chat", key="clear_chat"):
        # Clear all earlier messages except the system message
        st.session_state.messages = [
            {"role": "system", "content": system_message}
        ]


# region <--------- Use Case 2:  Rental Income Tax Calculator --------->

import pandas as pd
# from logics.crew_analysis import run_crew_analysis # CrewAi not compatible with ChromaDB on streamlit :(
from logics.rentalcalculatorlangchain import run_rental_analysis
import requests.exceptions

with rent:
    # def collect_rental_income_data():
    st.header("Residential Rental Income Tax Calculator")
    st.write("""
    Welcome! I’m here to help you easily calculate your taxable rent from residential property in Singapore. 
    Just share some details about your property income and expenses in the form below — no personal information needed, and everything stays private. Let’s get started!                              
    """)    
    st.warning('This form will only help your compute your taxable net rent from YA2022 owwards. If you need to compute your taxable rent for YA 2021 and before, please visit https://www.iras.gov.sg/quick-links/calculators to download the relevant calculator ')

    # Initialise session state for properties if it doesn't exist
    if 'properties' not in st.session_state:
        st.session_state.properties = []

    st.subheader('Step 1: Enter the property rental details')
    # Capped no. of properties that can be added to 10. Can be increased if nccy.
    num_properties = st.number_input("Number of properties", min_value=1, max_value=10)

    for i in range(num_properties):
        with st.container(border=True):
            st.subheader(f"Property {i+1}")
            
            # Initialise property in session state if it doesn't exist
            if i >= len(st.session_state.properties):
                st.session_state.properties.append({
                    "rental_income": 0.0,
                    "is_co_owned": False,
                    "ownership_share": 0.0,
                    "expenses": pd.DataFrame(columns=["Category", "Amount", "Description"])
                })
            
            property_info = st.session_state.properties[i]

            rent, share = st.columns(2) 

            with rent:

                property_info["rental_income"] = st.number_input(f"Rental Income", min_value=0.0, key=f"income_{i}", 
                                                                 value=property_info["rental_income"],
                                                                 help="Includes rent of the property, furniture and fittings and maintenance")
                
            with share:
                property_info["is_co_owned"] = st.checkbox(f"Co-owned", key=f"co_owned_{i}", value=property_info["is_co_owned"])
                if property_info["is_co_owned"]:
                    property_info["ownership_share"] = st.number_input(f"Your ownership share (%)", min_value=0.0, max_value=100.0, key=f"ownership_share_{i}", value=property_info["ownership_share"])

            
            expense_add, expense_update = st.columns([1, 2]) 
            # This column is to faciliate the adding and claiming of expenses
            # Can be removed and just rely on the datatable if preferred
            with expense_add:
                st.subheader("Add Expense")

                expense_category = st.selectbox("Category", ["Propety Tax", "Mortgage Loan Interest", "Fire Insurance", "Maintenance Fee", "Repairs","Agent Commission", "Others"], key=f"exp_cat_{i}")
                expense_amount = st.number_input("Amount", min_value=0.0, key=f"exp_amount_{i}")
                expense_description = st.text_input("Description", key=f"exp_desc_{i}")

                # Check if category is "Others" and description is empty
                if expense_category == "Others" and not expense_description:
                    st.error("Please provide a description for your 'Others' expense.")

                if st.button("Add Expense", key=f"add_exp_{i}"):

                
                    new_expense = pd.DataFrame({
                    "Category": [expense_category],
                    "Amount": [expense_amount],
                    "Description": [expense_description]
                    })
                    # Check if new_expense is empty or all-NA
                    # This is to address the FutureWarning that appears in the Terminal when run the app
                    if not new_expense.empty and not new_expense.isnull().all().all():
                        property_info["expenses"] = pd.concat([property_info["expenses"], new_expense], ignore_index=True)     
                    
            
        
            with expense_update:
                st.subheader("Expenses")
                st.write('You can edit the info in the datatable below, add or delete rows.')
                edited_df = st.data_editor(property_info["expenses"], num_rows="dynamic", key=f"expenses_editor_{i}")
                property_info["expenses"] = edited_df

                if st.button("Update Property", key=f"update_prop_{i}"):
                    st.session_state.properties[i] = property_info
                    st.success(f"Property {i+1} information updated!")


    if 'calculate_clicked' not in st.session_state:
        st.session_state.calculate_clicked = False

    # Function to handle property removal
    def remove_property(idx):
        del st.session_state.properties[idx]
        st.session_state.calculate_clicked = False

    # Function to clear all properties
    def clear_all_properties():
        st.session_state.properties = []
        st.session_state.calculate_clicked = False

    # Function to toggle calculate_clicked state
    def toggle_calculate():
        st.session_state.calculate_clicked = not st.session_state.calculate_clicked

    st.subheader('Step 2: Review the property rental details provided')
    st.write('To make changes, you can go back to Step 1 to update the property rental details')
    # This function is merely to trigger the toggle_calculate function
    if st.button("Show input summary", on_click=toggle_calculate):
        pass
    # Display the no. of properties updated
    if st.session_state.calculate_clicked:
        st.write("Properties submitted:", len(st.session_state.properties))
        
        for idx, prop in enumerate(st.session_state.properties):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"Property {idx+1}")
                    st.write(f"Rental Income: ${prop['rental_income']:,.2f}")
                    st.write(f"Number of Expenses: {len(prop['expenses'])}")
                    st.write(f"Co-owned: {'Yes' if prop['is_co_owned'] else 'No'}")
                    if prop['is_co_owned']:
                        st.write(f"Your ownership share: {prop['ownership_share']}%") 
                    st.write("Expenses:")
                    st.dataframe(prop['expenses'])
                    
                    # Calculate total expenses
                    total_expenses = prop['expenses']['Amount'].sum()
                    st.write(f"Total Expenses submitted: ${total_expenses:,.2f}")
                    
            
                with col2:
                    st.button("Remove Property", key=f"remove_prop_{idx}", on_click=remove_property, args=(idx,))
        
        # Copy info provided onto a property list object
        property_list = st.session_state.properties

        # Add a button to clear all properties
        st.button("Clear All Properties", on_click=clear_all_properties)

    st.subheader('Step 3: Generate a rental income report')
    # Button to trigger the Sequential analysis
    if st.button("Analyse Rental Income"):
        # First check if properties exist
        if not st.session_state.properties:
            st.error("No properties found. Please add property information first.")
        else:
            with st.spinner("Analysing rental income... This may take a few minutes."):
                try:

                    # Run the analysis with the provided path
                    # result = run_crew_analysis(property_list) # CrewAI script not used
                    result = run_rental_analysis(property_list)
                    result = result.replace("$", "\\$") # escape the $ character which may distort markdown formatting
                    
                    
                    st.markdown("## Analysis Results")
                    st.markdown(result)                   

                # Handle execptions gracefully        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Connection error occurred. Please check your internet connection.")
                    st.info("This tool requires internet access to perform the analysis.")
                
                except KeyError as e:
                    st.error(f"❌ Missing required environment variable: {str(e)}")
                    st.info("Please ensure all required environment variables are set in your .env file.")
                
                except FileNotFoundError as e:
                    st.error(f"❌ File not found: {str(e)}")
                    st.info("Please ensure all required files are in the correct location.")
                
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    st.info("If this persists, please check your setup and try again.")
