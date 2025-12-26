import streamlit as st
from ui_manager import UIManager

class App:
    def __init__(self):
        self.ui_manager = UIManager()

    def run(self):
        self.ui_manager.header()
        self.ui_manager.setup_page()
        self.ui_manager.sidebar()
        self.ui_manager.download_button()

def main():
    app = App()
    app.run()
    
if __name__ == "__main__":
    main()