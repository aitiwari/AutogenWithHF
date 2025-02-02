from autogen import AssistantAgent
import streamlit as st
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent



class TrackableRetrieveAssistantAgent(RetrieveAssistantAgent):
    def _process_received_message(self, message, sender, silent):
        if type(message)== str and sender.name =="Userproxy":
            with st.chat_message("user"):
                st.write(message)
        return super()._process_received_message(message, sender, silent)