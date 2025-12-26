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
    
    def file_uploader(self):
        """
        This method creates a file uploader in the Streamlit app.
        """
        uploaded_files = st.file_uploader(
            "Choose images to upload",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )
        return uploaded_files
    
    # button_text, data, file_name are kept random to check the UI later need to fix this
    def download_button(self, button_text="Download File", data=None, file_name="output.png"):
        """
        This method creates a download button in the Streamlit app.
        """
        # Use test data if no data is provided
        if data is None:
            data = b"Test data for download button"
        
        st.download_button(
            label=button_text,
            data=data,
            file_name=file_name,
            mime="image/png"
        )