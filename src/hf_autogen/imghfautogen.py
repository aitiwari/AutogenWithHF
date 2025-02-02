import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChatManager, GroupChat, ConversableAgent
from types import SimpleNamespace
import requests
import json
import os
import shutil
import random
import streamlit as st
import base64
from io import BytesIO

from src.agents.assistantagent import TrackableImageAssistantAgent
from src.agents.userproxyagent import TrackableUserProxyAgent

class APIModelClient:
    def __init__(self, config, **kwargs):
        self.device = config.get("device", "cpu")
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
        #self.api_url = "https://api-inference.huggingface.co/models/google/gemma-7b-it"  # Add the API URL to the config
        self.headers = {"Authorization": "Bearer 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"}  # Example: Add any required headers

        self.model_name = config.get("model")
        self.chat_index = 0

        self.conversion_mem = ""

        # self.tokenizer and self.model lines are removed or modified

    def create(self, params):
        conversation_history = ""

        for message in params["messages"]:
            prefix = ""
            if message["role"] == "system":
                prefix = f'Bot Description:\n'
            elif message["role"] == "user":
                prefix = f'User____:\n'
            else:
                prefix = f'Agent ({message["role"]}):\n'
            conversation_history += prefix + f'{message["content"]}\n\n'
        

        #try:
        #_input = f'Given the context of the last message: {params["messages"][-2]["content"]}\n\n\nHere is input on the context: {params["messages"][-1]["content"]}'


        #except Exception as e:
        #    print(e)
        #    _input = params["messages"][-1]["content"]

        input_data = {
            "inputs": conversation_history,
            # "parameters": {"return_full_text": False, "do_sample": False},
            # "options": {"wait_for_model": True, "use_cache": False}
            # Include any other parameters required by your API
        }

        # Sending the request to your model's API
        response = requests.post(self.api_url, json=input_data, headers=self.headers)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


    def message_retrieval(self, response):
        """Retrieve the messages from the response."""
        import io
        from PIL import Image
        image = Image.open(io.BytesIO(response.content))
        image_path = './imagegen/response.jpeg'
        image.save(image_path)
        # Open the image using PIL
        image = Image.open(image_path)

        # Display the image in Streamlit
        st.image(image, caption="Loaded Image", use_column_width=True)
        return [str(response.content)]

    def cost(self, response) -> float:
        """Calculate the cost of the response."""
        response.cost = 0
        return 0

    @staticmethod
    def get_usage(response):
        # returns a dict of prompt_tokens, completion_tokens, total_tokens, cost, model
        # if usage needs to be tracked, else None
        return {}


class APIModelClientWithArguments(APIModelClient):
    def __init__(self, config, hf_key, hf_url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large", **kwargs):
        self.device = config.get("device", "cpu")
        self.api_url = hf_url
        # self.api_url = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"  # Add the API URL to the config

        self.headers = {"Authorization": f"Bearer {hf_key}"}  # Example: Add any required headers

        self.model_name = config.get("model")
        self.chat_index = 0

        self.conversion_mem = ""
        

def hf_llmconfig(selected_model):
    llm_config = {
        "config_list": [{
            "model": selected_model,
            "model_client_cls": "APIModelClientWithArguments",
            "device": ""
        }]
    }
    st.session_state['llm_config'] = llm_config
    return llm_config
def UserAgent(name, llm_config, max_consecutive_auto_reply=1, code_dir="coding", use_docker=False, system_message="You are a helpful AI assistant"):
    llm_config = {
        "config_list": [{
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "model_client_cls": "APIModelClientWithArguments",
            "device": ""
        }]
    }
    user_agent = TrackableUserProxyAgent(
        name=name,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": code_dir,
            "use_docker": use_docker,
        },
        system_message=system_message,
        human_input_mode="NEVER"
    )

    user_agent.register_model_client(model_client_cls=APIModelClientWithArguments, hf_key=st.session_state["api_key"])

    return user_agent

def ModelAgent(name, llm_config, hf_url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large", system_message="", code_execution=False):
    default_system_message = """You are a helpful AI assistant for generating and manipulating images.
    """

    if system_message == "":
        system_message = default_system_message

    # llm_config = {
    #     "config_list": [{
    #         "model": "",
    #         "model_client_cls": "APIModelClientWithArguments",
    #         "device": ""
    #     }]
    # }
    llm_config =llm_config



    agent = TrackableImageAssistantAgent(
        name=name,
        llm_config=llm_config,
        system_message=system_message,
        code_execution_config=code_execution,
        
    )
    agent.register_model_client(model_client_cls=APIModelClientWithArguments, hf_key=st.session_state["api_key"], hf_url=hf_url)

    return agent


async def InitChat(user, agent, _input, summary_method="reflection_with_llm"):
    def clear_directory_contents(dir_path):
        try:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)  # Remove files and links
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directories
            shutil.rmtree(dir_path)
            print(f"All contents of '{dir_path}' have been removed.")
        except FileNotFoundError:
            pass

    #seed = random.randint(0, 99999)
    seed = 42
    #clear_directory_contents(f'./autogen_cache/{seed}')

    custom_cache = autogen.Cache({"cache_seed": seed, "cache_path_root": "autogen_cache"})

    await user.a_initiate_chat(
        agent,
        max_turns=1,
        message=_input,
        summary_method=summary_method,
        cache=custom_cache,
        
    )

    #clear_directory_contents(f'./autogen_cache/{seed}')    

def GroupChat(user, agents, _input, hf_key, hf_url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large", max_round=5):
    llm_config = {
            "config_list": [{
                "model": "",
                "model_client_cls": "APIModelClientWithArguments",
                "device": ""
            }]
        }

    groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=max_round, speaker_selection_method="round_robin", allow_repeat_speaker=False)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    manager.register_model_client(model_client_cls=APIModelClientWithArguments, hf_key=hf_key, hf_url=hf_url)
    InitChat(user, manager, _input)

#Write me a script to save the BTC chart from the past year to an image.

# if __name__ == "__main__":
#     print("Running as main")


 
 