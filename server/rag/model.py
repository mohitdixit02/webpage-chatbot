from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from rag.template import TemplateProvider
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Literal, Optional, Dict, Any
from pprint import pprint
import numpy as np
from numpy import dot
from numpy.linalg import norm

class QueryTypeStructModel(BaseModel):
    type: Annotated[Literal["casual", "query"], Field(description="Type of the user query")]

class CasualResponseStructModel(BaseModel):
    response: Annotated[str, Field(description="Response to the casual user query")]
    
class QueryResponseStructModel(BaseModel):
    answer: Annotated[Dict[str, Any],  Field(description="Answer to the user query based on the provided context in form of key-value pairs")]
    
class WikiKeywordResponseModel(BaseModel):
    keywords: Annotated[list, Field(description="List of relevant keywords extracted from the user query")]
    
class EmbedModel:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
    def get_model(self):
        return self.model
    
    def get_relevance_score(self, query: str, document: str):
        query_embd = self.model.embed_query(query)
        doc_embd = self.model.embed_query(document)
        
        cosine_sim = dot(np.array(query_embd), np.array(doc_embd)) / (norm(np.array(query_embd)) * norm(np.array(doc_embd)))
        return cosine_sim

class GenerateModel:
    def __init__(self):
        self.model = ChatHuggingFace(llm=HuggingFaceEndpoint(
            repo_id="meta-llama/Llama-3.1-8B-Instruct",
            task="conversational",
            max_new_tokens=500,
            temperature=0.2,
        ))
        self.template_provider = TemplateProvider()
        self.str_parser = StrOutputParser()
        
    def get_model(self):
        return self.model
    
    def get_query_type(self, query: str):
        print("Classifying query type...")
        try:
            query_parser = PydanticOutputParser(pydantic_object=QueryTypeStructModel)
            template = self.template_provider.get_query_type_template(instructions=query_parser.get_format_instructions())
            
            query_chain = template | self.model | query_parser
            res = query_chain.invoke(
                {"query": query},
                config={
                    "configurable": {"max_new_tokens": 100}
                }
            )
            return res.type
        except Exception as e:
            print("Error in query type classification:", e)
            return None
        
    def get_wiki_keywords(self, query: str):
        print("Extracting Wikipedia keywords...")
        try:
            wiki_parser = PydanticOutputParser(pydantic_object=WikiKeywordResponseModel)
            wiki_template = self.template_provider.get_wiki_keywords_template(
                instructions=wiki_parser.get_format_instructions()
            )
            
            wiki_chain = wiki_template | self.model | wiki_parser
            res = wiki_chain.invoke(
                {"query": query},
                config={
                    "configurable": {"max_new_tokens": 100}
                }
            )
            print("Extracted Keywords:", res)
            return res.keywords
        except Exception as e:
            print("Error in Wikipedia keyword extraction:", e)
            return []
        
    def generate(self, context: object, behaviour: str="Explain", mode: str="casual"):
        print("Generating response...")
        if mode == "casual":
            try:
                prompt = context.get("query")
                print("Active Mode: Casual Conversation")
                print("Casual mode prompt:", prompt)
                casual_parser = PydanticOutputParser(pydantic_object=CasualResponseStructModel)
                gen_template = self.template_provider.get_casual_template(instructions=casual_parser.get_format_instructions())
                gen_chain = gen_template | self.model | casual_parser
                gen_res = gen_chain.invoke(
                    {"query": prompt},
                    config={
                        "configurable": {"max_new_tokens": 500}
                    }
                )
                return gen_res.response
            except Exception as e:
                print("Error in casual response generation:", e)
                return None
        else:
            try:
                user_query = context.get("query")
                context_docs = context.get("context_docs", [])
                externalSearchFail = context.get("externalSearchFail", False)
                InPageSearchFail = context.get("InPageSearchFail", False)
                print("Active Mode: Query Response")
                print("External Search Failed:", externalSearchFail)
                print("In-Page Search Failed:", InPageSearchFail)
                print("Model behaviour:", behaviour)
                gen_parser = PydanticOutputParser(pydantic_object=QueryResponseStructModel)
                gen_template = self.template_provider.get_generation_template(
                    instructions=gen_parser.get_format_instructions(),
                    behaviour=behaviour,
                    externalSearchFail=externalSearchFail,
                    inPageSearchFail=InPageSearchFail
                )
                
                gen_res_chain = gen_template | self.model | gen_parser
                gen_res = gen_res_chain.invoke(
                    {
                        "query": user_query,
                        "context_docs": context_docs
                    },
                    config={
                        "configurable": {
                            "max_new_tokens": (800 if behaviour=="One-Line" else 3000)
                        }
                    }
                )
                return gen_res.answer
            except Exception as e:
                print("Error in query response generation:", e)
                return None
            