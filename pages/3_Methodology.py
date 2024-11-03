import streamlit as st
from streamlit_lottie import st_lottie
import requests
from helper_functions.utility import check_password
from logics.flowcharts import display_tax_relief_flowchart, display_rental_income_flowchart
from helper_functions.utility import check_password

# Check if the password is correct.  
if not check_password():  
    st.stop()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_methodology():
    # Configure page settings
    st.set_page_config(
        page_title="TaxEase Methodology",
        page_icon="🤖",
        layout="wide"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .highlight {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #4B0082;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section with Animation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🔍 TaxEase Methodology")
        st.subheader("Understanding What's Under the Hood")
    with col2:
        # Load animation
        lottie_url = "https://assets4.lottiefiles.com/packages/lf20_9gvkycqg.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200)

    # Tax Claim Relief Flow Section
    st.markdown("## 1. Tax Claim Relief Flow")
    
    st.markdown("### Input Collection")
    st.info("""
    The process begins by gathering essential user information through our intuitive interface. 
    The requested details are:
    
    - Citizenship status
    - Gender
    - Marital status
    - Parenthood status
    - Employment status
     
    These details form the foundation for determining tax relief eligibility and ensuring accurate 
    recommendations tailored to each user's unique situation.
    """)

    st.markdown("### Eligibility Filtering")
    st.info("""
    Our filtering system identifies and narrows down relief options strictly applicable to the user's profile provided:
            
    1. The system queries a tax relief table provided in a CSV file.
    2. It identifies tax reliefs that match the profile inputs provided by the user.
    3. The profile inputs and matched tax reliefs serve as the initial query and response in the chat conversation.
    4. This provides context and facilitates further exploration of relevant reliefs. 
    
    This approach reduces possible mismatches that could arise from the probabilistic nature of LLMs' responses, ensuring higher accuracy in relief recommendations.
    """)

    st.markdown("### Output Generation")
    st.success("""
    The final stage of our tax relief advisory process involves an interaction system where users can:
    
    1. Review their filtered list of eligible reliefs
    2. Identify specific reliefs of interest
    3. Obtain detailed information through our interactive chatbot
    4. Access comprehensive explanations powered by our retrieval-augmented generation (RAG) LLM system
    5. Receive guidance based on authentic tax relief information extracted directly from IRAS website
    """)

    # Display flowchart
    st.markdown("### Tax Relief Advisory Process Visualisation")
    st.write("Below is a detailed flowchart of our tax relief advisory process:")
    display_tax_relief_flowchart()

    st.markdown("## 2. Rental Income Calculation Flow")
    
    st.markdown("### Property Details Input")
    st.info("""
    Please provide the following essential information for each rental property:

    - Property rental income details
    - Co-ownership status (if applicable)
    - Your ownership share percentage
    - All property-related expenses
    
    This information helps us accurately assess your rental income tax situation.
    """)

    st.markdown("### Analysis Process")
    st.info("""
    Our intelligent tax analysis system follows these steps:

    1. Initial Setup
       - Creates a specialized vector store for tax guidelines
       - Establishes QA chain for accurate tax interpretations
       - Loads latest IRAS tax guidelines and regulations

    2. Comprehensive Analysis
       - Tax Specialist Review:
         • Evaluates each expense category
         • Determines tax deductibility
         • Performs detailed tax research when needed
       - Computation Methods:
         • Actual Expense Method: Detailed expense deductions
         • Simplified Method: 15% deemed expenses plus mortgage interest
       - Strategy Assessment: Identifies optimal tax approach
    """)

    st.markdown("### Final Report & Recommendations")
    st.success("""
    Our system generates a detailed final report including:

    1. Property-Specific Analysis
       - Complete breakdown of rental income
       - Detailed expense categorization
       - Ownership share calculations

    2. Method Comparison
       - Side-by-side analysis of actual vs. simplified methods
       - Clear presentation of tax implications for each approach
       - Highlighted advantages and considerations

    3. Strategic Guidance
       - Recommended calculation method based on your situation
       - Key compliance requirements and deadlines
       - Essential record-keeping guidelines
       - Tips for future tax optimization
    """)

    # Display flowchart
    st.markdown("### Rental Income Calculation Process Visualization")
    st.write("Below is a detailed flowchart of our rental income calculation process:")
    display_rental_income_flowchart()

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align: center'>
            <p>Engineered with precision by TaxEase</p>
            <p style='font-size: 0.8em'>Version 1.0.0</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_methodology()
