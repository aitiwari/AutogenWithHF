import asyncio
from src.hf_autogen.imghfautogen import APIModelClientWithArguments,ModelAgent, UserAgent, InitChat
from src.agents.assistantagent import TrackableAssistantAgent
from src.agents.userproxyagent import TrackableUserProxyAgent
import streamlit as st


class ImageGeneration:
    def __init__(self, assistant_name, user_proxy_name, llm_config, problem):
        # self.assistant = TrackableAssistantAgent(name=assistant_name,
        #                                          system_message="""you are helpful assistant. Reply "TERMINATE" in 
        #                                          the end when everything is done """,
        #                                          human_input_mode="NEVER",
        #                                          llm_config=llm_config,
        #                                          )
        
        # self.user_proxy = TrackableUserProxyAgent(name=user_proxy_name,
        #                                           system_message="You are Admin",
        #                                           human_input_mode="NEVER",
        #                                           llm_config=llm_config,
        #                                           code_execution_config=False,
        #                                           is_termination_msg=lambda x: x.get("content", "").strip().endswith(
        #                                               "TERMINATE"))
        
        
        self.user = UserAgent(name=user_proxy_name,llm_config=llm_config)
        self.assistant = ModelAgent(name=assistant_name,
                                llm_config=llm_config,
                                hf_url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large",
                                system_message="You are a friendly AI assistant. Your job is to generate image with HD quality")

        self.problem = problem
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    # async def initiate_chat(self):
    #     await InitChat(self.user, self.assistant, self.problem)

    def run(self):
        self.loop.run_until_complete(InitChat(self.user, self.assistant, self.problem))