import streamlit as st

class UIManager:
    
    def setup_page(self):
        """
        this method sets up the Streamlit page configuration. 
        It defines the page title, icon, layout, and initial sidebar state.
        """
        st.set_page_config(
            page_title="Image Stacking App",
            page_icon="🌆",
            layout="centered",
            initial_sidebar_state="auto"
        )
    def header(self):
        """
        This method creates the header section of the Streamlit app.
        """
        st.title("📸 Image Stacking Application 📸")
        st.markdown("*Upload your images to stack them*")
        
    def sidebar(self):
        """
        This method creates the sidebar section of the Streamlit app.
        """
        st.sidebar.title("Options")
        st.sidebar.markdown("Adjust your settings here.")