from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from pydantic import BaseModel
from apikey import OPENAI_API_KEY
import os
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY
loader=PyPDFLoader('./Docs/ChatGPT_wikipedia.pdf')
index=VectorstoreIndexCreator().from_loaders([loader])

app=FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

class Item(BaseModel):
    query:str

@app.get('/')
def read_root():
    return {"Hello": "world"}
@app.post('/')
def answer_query(item:Item):
    try:
        response=index.query(item.query)
        return response
    except:
        return {"messgage":"Some error happened"}