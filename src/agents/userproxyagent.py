from autogen import UserProxyAgent
import streamlit as st
import base64
from io import BytesIO


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        
        if type(message)==str and sender.name == 'Image_Assistant':
            with st.chat_message('ai'):
                st.image('./imagegen/response.jpeg')

        else :
            with st.chat_message('ai'):
                st.write(message)
        return super()._process_received_message(message, sender, silent)
