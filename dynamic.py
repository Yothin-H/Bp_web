import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Custom Theme Toggle for Main Area", page_icon="🎨", layout="wide")

# Sidebar for theme selection
theme_choice = st.sidebar.radio("Select Theme:", ("Light Mode", "Dark Mode"))

# Set CSS based on user choice
if theme_choice == "Dark Mode":
    main_area_bg_color = "#0E1117"  # Dark background color for the main area
    main_area_text_color = "#FFFFFF"  # Light text color for the main area
else:
    main_area_bg_color = "#FFFFFF"  # Light background color for the main area
    main_area_text_color = "#000000"  # Dark text color for the main area

# Inject custom CSS to change the background color of the main content area only
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {main_area_bg_color} !important;
        color: {main_area_text_color} !important;
    }}
    .css-1d391kg {{
        background-color: inherit !important;  /* Sidebar retains its original style */
    }}
    .css-18e3th9 {{
        background-color: inherit !important;  /* Top bar retains its original style */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Sidebar")
st.sidebar.write("This is the sidebar content. Sidebar color remains unchanged.")

# Main Area content
st.write("## Main Area")
st.write("This is the main area content in the selected theme.")
st.write("You can add more content here, and its background will change according to the theme.")
