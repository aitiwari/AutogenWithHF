import asyncio
from src.hf_autogen.hfautogen import APIModelClientWithArguments,ModelAgent, UserAgent, InitChat
from src.agents.assistantagent import TrackableAssistantAgent
from src.agents.userproxyagent import TrackableUserProxyAgent
import streamlit as st


class TexGeneration:
    def __init__(self, assistant_name, user_proxy_name, llm_config, problem):
        self.assistant = TrackableAssistantAgent(name=assistant_name,
                                                 system_message="""you are helpful assistant. Reply "TERMINATE" in 
                                                 the end when everything is done """,
                                                 human_input_mode="NEVER",
                                                 llm_config=llm_config,
                                                 )
        
        self.user_proxy = TrackableUserProxyAgent(name=user_proxy_name,
                                                  system_message="You are Admin",
                                                  human_input_mode="NEVER",
                                                  llm_config=llm_config,
                                                  code_execution_config=False,
                                                  is_termination_msg=lambda x: x.get("content", "").strip().endswith(
                                                      "TERMINATE"))
        

        self.user = UserAgent("user_proxy",hf_key=st.session_state['api_key'])
        self.assistant = ModelAgent("assistant",
                                hf_key=st.session_state['api_key'],
                                system_message="You are a friendly AI assistant.")

        self.problem = problem
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    # async def initiate_chat(self):
    #     await InitChat(self.user, self.assistant, self.problem)

    def run(self):
        self.loop.run_until_complete(InitChat(self.user, self.assistant, self.problem))