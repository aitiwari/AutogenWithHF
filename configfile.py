from configparser import ConfigParser


class Config:
  def __init__(self, config_file="configfile.ini"):
    self.config = ConfigParser()
    self.config.read(config_file)

  def get_llm_options(self):
    return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")

  def get_usecase_options(self):
    return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")

  def get_text_hf_model_options(self):
    return self.config["DEFAULT"].get("TEXT_HF_MODEL_OPTIONS").split(", ")
  
  def get_img_hf_model_options(self):
    return self.config["DEFAULT"].get("IMG_HF_MODEL_OPTIONS").split(", ")

  def get_page_title(self):
    return self.config["DEFAULT"].get("PAGE_TITLE")

