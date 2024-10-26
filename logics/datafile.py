import streamlit as st
import pandas as pd


# Path to read the relief table in csv format
filepath = './data/relief_table.csv'

# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv(filepath) 

# Check if 'df' is already in session state, if not, load it
if 'relief_df' not in st.session_state:
    st.session_state.relief_df = load_data()  # Persist the DataFrame in session_state

# Access the persisted DataFrame
relief_df = st.session_state.relief_df

# The function to filter and return column names with value == 1
def filter_and_get_reliefs(citizenship=None, gender=None, maritial_status=None, employment=None, children=None):
    # Start with the full DataFrame and apply filters only if the corresponding parameter is provided
    filtered_df = relief_df
    
    # The following sequential approach ensures that if any of the 5 criteria isn't provided, the filtering will still work
    if citizenship:
        filtered_df = filtered_df[filtered_df['citizenship'] == citizenship]
    if gender:
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    if maritial_status:
        filtered_df = filtered_df[filtered_df['maritial_status'] == maritial_status]
    if employment:
        filtered_df = filtered_df[filtered_df['employment'] == employment]
    if children:
        filtered_df = filtered_df[filtered_df['children'] == children]

    # If the filtered DataFrame is not empty, find the columns where value == 1
    if not filtered_df.empty:
        # Iterate over all rows in the filtered DataFrame and get the columns with value == 1
        relief_columns = set()  # Use a set to avoid duplicates
        for _, row in filtered_df.iterrows():
            # Add all column names where value == 1 to the set
            relief_columns.update(row[row == 1].index.tolist())
            
        # sort the list of applicable reliefs
        eligible_relief = sorted(list(relief_columns))
        # Join the reliefs with bullet points
        reliefs_bulleted = "\n\n"+"\n\n".join([f"• {relief}" for relief in eligible_relief])
        response = f"""
        Based on your inputs, you're eligible for the following tax reliefs:
        
        {reliefs_bulleted}\n\nWould you like to find out more about any of the relief types listed above?
        """        
        return response
    else:
        return f'No matching tax relief was found. 😕'


# The function to captures the inputs from the user to be provided to the LLM as context
def capture_and_store(citizenship=None, gender=None, maritial_status=None, employment=None, children=None):
    inputs = """I have been in Singapore for more than 183 days in the year. My other details are:"""
    if citizenship:
        inputs = inputs  + f"\n\n- My citizenship is {citizenship}."
    if gender:
        inputs = inputs  + f"\n\n- My gender is {gender}."
    if maritial_status:
        inputs = inputs + f"\n\n- My martial status is {maritial_status}."
    if children:
        inputs = inputs + f"\n\n- I indicated '{children}' to the question on whether I have children."
    if employment:
        inputs = inputs + f"\n\n- My employment status is {employment}."

    return inputs





