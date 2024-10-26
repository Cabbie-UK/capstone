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
    3. These matched tax reliefs serve as the initial query and response in the chat conversation.
    4. This provides context and facilitates further exploration of relevant reliefs. 
    
    This approach reduces possible mismatches that could arise from the probabilistic nature of LLMs' responses, ensuring higher accuracy in recommendations.
    """)

    st.markdown("### Output Generation")
    st.success("""
    The final stage of our tax relief advisory process involves an interaction system where users can:
    
    1. Review their filtered list of eligible reliefs
    2. Identify specific reliefs of interest
    3. Obtain detailed information through our interactive chatbot
    4. Access comprehensive explanations powered by our RAG LLM system
    5. Receive guidance based on authentic tax relief information extracted directly from IRAS website
    """)

    # Display flowchart
    st.markdown("### Tax Relief Advisory Process Visualisation")
    st.write("Below is a detailed flowchart of our tax relief advisory process:")
    display_tax_relief_flowchart()

    # Rental Income Calculation Flow Section
    st.markdown("## 2. Rental Income Calculation Flow")
    
    st.markdown("### Input Collection")
    st.info("""
    Our rental income assessment begins with a comprehensive data gathering of property rental details:

    - Gross Rental Income
    - Ownership percentage
    - Detailed rental expense records
    """)

    st.markdown("### Income Calculation")
    st.info("""
    Our system employs a precise calculation methodology that:
    
    1. Considers all deductible expenses that can be claimed against rental income
    2. Determines the user's portion of total rental income based on documented ownership share
    3. Calculates the final taxable rental amount with adjustments for the user's specific situation
    """)

    st.markdown("### Recommendations")
    st.success("""
    The final stage leverages our advanced analytics tool to:
    
    1. Employ a multi-agent LLM (CrewAI) for comprehensive data analysis
    2. Review all submitted information systematically
    3. Identify optimal tax-efficient expense claim methods
    4. Provide comprehensive analysis of potential outcomes
    5. Outline specific benefits for each recommended approach
    6. Ensure maximum legitimate tax advantages
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
