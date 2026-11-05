
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)
st.title("🏥 Healthcare Insights Dashboard")

st.header("CS 1301 - Web Development Lab 2")

st.write("Welcome to my Healthcare Insights Dashboard! 📊")

st.write(
    "This website explores patient visits across four "
    "healthcare departments: General Medicine, Pediatrics, "
    "Dermatology, and Cardiology."
)

st.write(
    "Navigate to the Visuals page to explore patient "
    "distribution and monthly healthcare trends."
)
# INTRODUCTORY TEXT
st.write("""
This application is designed to collect and visualize data.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Visuals Page**: Navigate to the Visuals page to explore patient 
    distribution and monthly healthcare trends.
- **Survey Page**: Share your experiences with healthcare services.

""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
