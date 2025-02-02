from autogen import AssistantAgent
import streamlit as st


class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        if message and type(message)== str and sender.name =="Userproxy":
            with st.chat_message("user"):
                st.write(message)
        
                
        return super()._process_received_message(message, sender, silent)


