import streamlit as st
from configfile import Config
from src.hf_autogen.hfautogen import hf_llmconfig
from src.streamlitui.loadui import LoadStreamlitUI
from src.usecases.textgen import TexGeneration
from src.usecases.imggen import ImageGeneration



# MAIN Function START


if __name__ == "__main__":
    # config
    obj_config = Config()
    # load ui
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    # # Configure LLM
    # obj_llm_config = GroqLLM(user_controls_input=user_input)
    # obj_llm_config.groq_llm_config()
    # llm_config = st.session_state['llm_config']

    # userInput
    problem = st.chat_input("Start Chat ")
    
    # configure llm
    hf_llmconfig(selected_model = user_input["selected_hf_model"])
    if 'config_list' in st.session_state['llm_config'] : 
        llm_config = st.session_state['llm_config']

    
    if user_input['selected_usecase'] == "Text Generation":
        st.subheader("Text generation")
        if problem:
            with st.chat_message("user"):
                st.write(problem)
            
            
            obj_txt_gen = TexGeneration(assistant_name="Assistant", user_proxy_name='Userproxy',
                                                    llm_config=llm_config,
                                                    problem=problem)
            obj_txt_gen.run()
    
    elif user_input['selected_usecase'] == "Image Generation": 
        st.subheader("Image generation")
        
        if problem:
            with st.chat_message("user"):
                st.write(problem)
                
           
            obj_img_gen = ImageGeneration(assistant_name="Image_Assistant", user_proxy_name='Userproxy',
                                                    llm_config=llm_config,
                                                    problem=problem)
            obj_img_gen.run()
            
            # with st.chat_message('ai'):
            #     st.image(image.open('./imagegen/response.jpeg'))
               
            
            
            


