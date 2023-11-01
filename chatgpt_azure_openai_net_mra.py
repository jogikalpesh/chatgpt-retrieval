import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.llms import OpenAI
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI

from langchain.vectorstores import Chroma

import constants


os.environ["OPENAI_API_TYPE"] = constants.OPENAI_API_TYPE
os.environ["OPENAI_API_BASE"] = constants.OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
os.environ["OPENAI_API_VERSION"]=constants.OPENAI_API_VERSION

openai.api_type = constants.OPENAI_API_TYPE
openai.api_base = constants.OPENAI_API_BASE
openai.api_version = constants.OPENAI_API_VERSION
openai.api_key = constants.OPENAI_API_KEY




# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True
PERSIST_DIRECTORY = "persist-net-mra"

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

embedding = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    deployment="base-text-embedding-ada-002",
    chunk_size=1,
    request_timeout=120) 

if PERSIST and os.path.exists(PERSIST_DIRECTORY):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding)
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = TextLoader("data/dotnet-mra/documentation.md") # Use this line if you only need data.txt
  # loader = DirectoryLoader("data/dotnet-mra/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":PERSIST_DIRECTORY},embedding=embedding).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])



chain = ConversationalRetrievalChain.from_llm(
   llm= AzureChatOpenAI(
          openai_api_key=constants.OPENAI_API_KEY,
          deployment_name="base-gpt35-turbo",
          model_name="gpt-35-turbo"
        ),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
  verbose=True
)

chat_history = []
while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  result = chain({"question": query, "chat_history": chat_history})
  print(result['answer'])

  chat_history.append((query, result['answer']))
  query = None
