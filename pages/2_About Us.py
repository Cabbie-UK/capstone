import streamlit as st
from streamlit_lottie import st_lottie
import requests
from helper_functions.utility import check_password

#Check if the password is correct.  
if not check_password():  
    st.stop()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_documentation():
    # Configure page settings
    st.set_page_config(
        page_title="TaxEase Documentation",
        page_icon="🤖",
        layout="wide"
    )

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
        </style>
    """, unsafe_allow_html=True)

    # Header Section with Animation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🤖 TaxEase")
        st.subheader("Intelligent Tax Advisory Solutions")
    with col2:
        # Load animation
        lottie_url = "https://assets4.lottiefiles.com/packages/lf20_9gvkycqg.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200)

    # Project Overview
    st.markdown("## 🎯 Project Overview")
    st.write("""
    Welcome to TaxEase, your comprehensive AI-powered tax assistant for navigating Singapore's 
    tax system. We leverage advanced artificial intelligence to provide accurate, timely, and 
    personalized tax guidance, making tax compliance straightforward and efficient.
    """)

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✨ Features", 
        "🔧 Technical Stack", 
        "📚 Data Sources", 
        "⚠️ Important Notes",
        "🚀 Future Plans"
    ])

    with tab1:
        st.markdown("### Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💡 Tax Relief Advisory")
            st.markdown("""
            - Personalised eligibility assessment
            - Smart filtering based on user profile
            - Real-time chat interface for queries
            - Comprehensive relief explanations
            - Interactive Q&A support
            """)
            
        with col2:
            st.markdown("#### 🏠 Rental Income Analysis")
            st.markdown("""
            - Multi-property support
            - Expense tracking and categorisation
            - Co-ownership calculations
            - Detailed analysis reports
            - Maximise legitimate tax deductions
            """)

    with tab2:
        st.markdown("### Technical Architecture")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Frontend Technology")
            st.code("""
            - Streamlit Framework
            - Dynamic Form Processing
            - Real-time State Management
            - Responsive Interface Design
            """)
            
        with col2:
            st.markdown("#### Backend & AI Infrastructure")
            st.code("""
            - LangChain Framework
            - ChromaDB Vector Store
            - OpenAI Embedding Systems
            - Pandas
            """)

    with tab3:
        st.markdown("### Data Sources")
        st.info("""
        Our system synthesizes information from authoritative sources to ensure accuracy:
        
        1. **IRAS Official Documentation**
           - Comprehensive tax relief guidelines
           - Current rental income regulations
                   
        2. **Knowledge Base Infrastructure**
           - Vectorized tax information repository
           - Curated response database
           - Validated use-case scenarios
        
        3. **User Analytics**
           - Profile-specific parameters
           - Property portfolio information
           - Expense tracking metrics
        """)

    with tab4:
        st.markdown("### Important Information")
        st.warning("""
        - This platform serves as an educational and advisory tool - all final tax matters should be verified with IRAS
        - System compatibility: YA2022 onwards
        - For official tax inquiries, please utilize these IRAS channels:
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            🌐 **Digital Channels**
            - Interactive Support: [IRAS LiveChat](https://go.gov.sg/iras-livechat)
            - Secure Portal: [MyTax Mail](https://mytax.iras.gov.sg)
            """)
        with col2:
            st.markdown("""
            📞 **Contact Center**
            - Domestic: 1800 356 8300
            - International: (+65) 6356 8300
            """)

    with tab5:
        st.markdown("### Development Roadmap")
        
        planned_features = {
            "Feature Expansion": [
                "Business Tax Calculator",
                "GST Registration Advisor",
                "Tax Planning Tools",
                "Update knowledge base with upcoming budget changes"
            ],

            "Code Upgrades": [
                "Enhance info retrieval flow for efficiency",
                "Modularisation for better organisation and reusability of code",
                "Optimise resources and reduce overheads for perfomance"
            ],
        }
        
        for category, features in planned_features.items():
            st.markdown(f"#### {category}")
            for feature in features:
                st.markdown(f"- {feature}")

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
    show_documentation()