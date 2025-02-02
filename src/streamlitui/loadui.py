import streamlit as st
from configfile import Config  # Import the Config class


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()  # Create a Config instance
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        with st.sidebar:
            
            # Use case selection
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
             # Get options from config
            llm_options = self.config.get_llm_options()
            self.user_controls["selected_llm"] = st.selectbox("", llm_options)
           
            # model selection 
            if self.user_controls["selected_usecase"] == "Text Generation":
                
                model_options = self.config.get_text_hf_model_options()
                self.user_controls["selected_hf_model"] = st.selectbox("Select Model", model_options)
            elif self.user_controls["selected_usecase"] == "Image Generation":
                model_options = self.config.get_img_hf_model_options()
                self.user_controls["selected_hf_model"] = st.selectbox("Select Model", model_options)
                
            # API key input
            st.session_state['api_key'] = st.text_input("API Key",type="password")
            
        return self.user_controls
