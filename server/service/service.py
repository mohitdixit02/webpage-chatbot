from rag.webloader import WebPageContentLoader
from rag.chroma import ChromaDatabase
from rag.model import GenerateModel
from config import logger
from reqModel.main import UserQueryRequest

class Service:
    def __init__(self):
        self.wb_loader = WebPageContentLoader()
        self.db = ChromaDatabase()
        self.gen_model = GenerateModel()

    def load_web_page_data(self, url: str):
        doc_exist = self.db.check_web_page(url)
        if doc_exist:
            logger.info("Web page already in the db")
            return {
                "status": True,
                "message": "Web page data already exists in the database."
            }
        else:
            docs = self.wb_loader.load_page_data(url)
            if docs is None:
                return {
                    "status": False,
                    "message": "Failed to load web page data."
                }
            else:
                res = self.db.add_docs(docs)
                if res is not None:
                    return {
                        "status": True,
                        "message": "Web page data loaded and added to the database."
                    }
                else:
                    return {
                        "status": False,
                        "message": "Failed to add web page data to the database."
                    }
            
    def handle_user_query(self, queryObj : UserQueryRequest):
        query_type = self.gen_model.get_query_type(queryObj.query)
        if query_type is None:
            return {
                    "status": False,
                    "data": "Failed to classify query type."
                }
        if query_type == "casual":
            logger.info("Casual conversation mode")
            res = self.gen_model.generate(
                context={
                    "query": queryObj.query
                }, 
                behaviour=queryObj.behaviour, 
                mode="casual"
            )
            return {
                "status": True,
                "data": res
            }
        else:
            query_docs = self.db.retrieve_docs(
                queryObj.query, 
                queryObj.url, 
                k=5,
                acceptable_relevance_score=0.4,
                relevance_score_threshold=0.6
            )
            InPageSearchFail = (len(query_docs) == 0)
            logger.info(f"External Search Enabled: {queryObj.externalSearch}")
            logger.info(f"In-Page Search Failed: {InPageSearchFail}")
            wiki_docs = []
            if queryObj.externalSearch or InPageSearchFail:       
                wiki_keywords = self.gen_model.get_wiki_keywords(queryObj.query)     
                wiki_docs = self.wb_loader.load_wikipedia_data(
                    wiki_keywords,
                    top_k=2,
                    acceptable_relevance_score=0.4,
                    relevance_score_threshold=0.75
                )
                
            context_docs = []
            for doc in query_docs:
                context_docs.append(doc.page_content)
                
            for doc in wiki_docs:
                context_docs.append(doc.page_content)
            
            logger.info(f"Context Documents Total Length: {len(context_docs)}")
            res = self.gen_model.generate(
                context={
                    "query": queryObj.query,
                    "context_docs": context_docs,
                    "externalSearchFail": (len(wiki_docs) == 0 and (queryObj.externalSearch or InPageSearchFail)),
                    "InPageSearchFail": (len(query_docs) == 0)
                }, 
                behaviour=queryObj.behaviour, 
                mode="query"
            )
            if res is None:
                return {
                    "status": False,
                    "data": "Failed to generate response for the user query."
                }
            return {
                "status": True,
                "data": res
            }