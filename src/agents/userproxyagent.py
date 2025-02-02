from autogen import UserProxyAgent
import streamlit as st


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name.lower()):
            if type(message)==str:
                st.write(message)
            else :
                st.write(message['content'])
        return super()._process_received_message(message, sender, silent)
