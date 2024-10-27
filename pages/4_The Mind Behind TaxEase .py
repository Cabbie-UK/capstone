import streamlit as st
from streamlit_lottie import st_lottie
import requests
from helper_functions.utility import check_password

# Check if the password is correct
if not check_password():
    st.stop()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_developer_profile():
    # Configure page settings
    st.set_page_config(
        page_title="Developer Profile - TaxEase",
        page_icon="👨‍💻",
        layout="wide"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #4B0082;
            margin-top: 2rem;
        }
        .highlight {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #f8f9fa;
        }
        .profile-section {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .section-divider {
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section with Animation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("👨‍💻 Meet the Developer")
        st.subheader("Bringing TaxEase to Life")
    with col2:
        # Load developer animation
        lottie_url = "https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200)

    # Profile Section
    st.markdown("## 👋 About Me")
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            Hi, I'm **Kah Boon** from IRAS' Taxpayer Experience Division, where I focus on Service Analytics. 
            I graduated with a Master of IT in Business (Analytics) from SMU in 2024 and am passionate about 
            using analytics to make a real-world impact with a user-centered approach.
            """)
            
            st.info("""
            I would love to connect, collaborate, or discuss any analytics initiatives—schedule permitting! 
            Feel free to reach me on Teams or Skype at kwa_kah_boon@iras.gov.sg! 😊
            """)

    # Technical Skills Section
    st.markdown("## 🎯 Technical Skills & Expertise")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Analytics & Data Science")
        st.markdown("""
        - Data Analysis & Visualisation
        - Machine Learning
        - Service Analytics
        """)
        
    with col2:
        st.markdown("### Development & Tools")
        st.markdown("""
        - AI/ML Frameworks (scikit-learn, Keras, PyCaret, TidyModels)
        - Data Visualisation and Business Intelligence (Tableau, Power BI, Streamlit, R Shiny)
        - Database Management (SQL)
        """)

    # Vision Section
    st.markdown("## 💡 Vision for TaxEase")
    st.success("""                          
    My vision for TaxEase is to revolutionise tax advisory services through:
    
    - **User-Centered Design**: Creating intuitive interfaces that make tax matters accessible
    - **Data-Driven Insights**: Leveraging analytics to provide personalised guidance
    - **Continuous Innovation**: Staying ahead with the latest technology trends
    - **Impactful Solutions**: Making a real difference in taxpayers' experiences
    """)

    # Credits Section
    st.markdown("## 🙏 Acknowledgements")
    st.info("""
    **Credit on the development of TaxEase:**
    
    - **Nick Tan**: Instructor for AI Champions Bootcamp, Knowledgeable, Clear and Helpful
    - **Fellow Bootcamp Participants**: For their valuable advice and shared experiences
    - **Open-source LLMs** (Claude, Gemini and ChatGPT): For the insightful interactions and learning opportunities throughout this journey. Lol!
    """)

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align: center'>
            <p>Let's connect and make tax services better together!</p>
            <p style='font-size: 0.8em'>TaxEase Developer Profile</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_developer_profile()