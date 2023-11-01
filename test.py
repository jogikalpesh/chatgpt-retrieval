import openai
from langchain.llms import AzureOpenAI
import os
import constants


openai.api_type = constants.OPENAI_API_TYPE
openai.api_base = constants.OPENAI_API_BASE
openai.api_version = constants.OPENAI_API_VERSION
openai.api_key = constants.OPENAI_API_KEY


os.environ["OPENAI_API_VERSION"]=constants.OPENAI_API_VERSION

llm = AzureOpenAI(
    openai_api_key=constants.OPENAI_API_KEY,
    deployment_name="base-davinci-002",
    model_name="davinci-002", 
)
print(llm("how much time it takes to reach mars from earth?"))