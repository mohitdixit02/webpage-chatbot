from langchain_community.document_loaders import WebBaseLoader
from langchain_community.retrievers import WikipediaRetriever
from rag.model import EmbedModel
from pprint import pprint
from typing import TypedDict

class WebPageContentLoader:
    def __init__(self):
        self.embd_model = EmbedModel()
        pass
    
    def load_page_data(self, url):
        try:
            print(f"Loading data from {url}...")
            docs = WebBaseLoader(url).load()
            print(f"Loaded {len(docs)} documents from {url}.")
            return docs
        except Exception as e:
            print(f"Error loading data from {url}:", e)
            return None
        
    def load_wikipedia_data(self, keywords, top_k=3, acceptable_relevance_score: float=0.5, relevance_score_threshold : float=0.5):
        try:
            print(f"Loading Wikipedia data for keywords...")
            wiki_retrv = WikipediaRetriever(
                language="en",
                top_k=top_k,
            )
            
            disimilar_keywords = []
            for kw in keywords:
                if all(self.embd_model.get_relevance_score(kw, existing_kw) < relevance_score_threshold for existing_kw in disimilar_keywords):
                    disimilar_keywords.append(kw)
            
            print(f"Dissimilar Keywords selected for Wikipedia search: {disimilar_keywords}")
            print("Acceptable Relevance Score:", acceptable_relevance_score)
            docs = []
            for keyword in disimilar_keywords:
                print(f"Fetching articles for keyword: {keyword}")
                doc_colln = wiki_retrv.invoke(keyword)
                docs.extend(doc_colln)
            
            print(f"Loaded {len(docs)} documents from Wikipedia for keywords.")
            print("Filtering Wiki documents based on relevance score threshold...")

            # Checking the relevance of every document with respect to 
            # the most relevant document fetched based on the keywords
            doc_with_scores = []
            top_score = 0
            for doc in docs:
                score = self.embd_model.get_relevance_score((" ").join(disimilar_keywords), doc.page_content)
                print(f"Wiki Document Title: {doc.metadata.get('title')}, Relevance Score: {score}")
                top_score = max(top_score, score)
                if(score >= acceptable_relevance_score):
                    doc_with_scores.append({   
                        "doc": doc,
                        "score": score,
                    })
                
            filtered_docs = [
                s["doc"]
                for s in doc_with_scores
                if s["score"] >= relevance_score_threshold * top_score
            ]
            
            print(f"{len(filtered_docs)} wiki documents passed the relevance score threshold of {relevance_score_threshold}.")
            for doc in filtered_docs:
                print(f"Wiki Document '{doc.metadata.get('title')}' passed the threshold.")
                            
            return filtered_docs
        
        except Exception as e:
            print(f"Error loading Wikipedia data for keywords {keywords}:", e)
            return []