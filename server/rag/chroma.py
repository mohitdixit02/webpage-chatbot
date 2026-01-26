from langchain_chroma import Chroma
from langchain_classic.schema import Document
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from rag.model import EmbedModel
import re

class ChromaDatabase:
    def __init__(self):
        self.embed_model = EmbedModel()
        self.db = Chroma(
            persist_directory="./db/chroma_db",
            collection_name="web_scripts",
            embedding_function=self.embed_model.get_model()
        )
        self.txtsplitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=0,
            separators=["\n\n", "\n", '. ', '.'],
            keep_separator=False
        )
    
    def preprocess_text(self, text):
        print("Preprocessing text...")
        text_remv_ws = re.sub(r'\s+', ' ', text).strip()
        splt_txt = self.txtsplitter.split_text(text_remv_ws)
        return splt_txt
        
    def load_db_content(self):
        res = self.db.get()
        return res
    
    def add_docs(self, scripts, auto_compress=True, compress_count=20):
        docs_list = []
        print("Adding documents to Chroma DB...")
        print(f"Total scripts to add: {len(scripts)}")
        for doc in scripts:
            doc_metadata = doc.metadata
            docs_chunks = self.preprocess_text(doc.page_content)
            for j, chunk in enumerate(docs_chunks):
                chunk_metadata = doc_metadata.copy()
                chunk_metadata.update({
                    "chunk_index": j,
                })
                print(f"Adding chunk {j + 1}/{len(docs_chunks)} for document with metadata: {doc_metadata}")
                docs_list.append(
                    Document(
                        page_content=chunk,
                        metadata=chunk_metadata
                    )
                )
        
        self.db.add_documents(documents=docs_list)
        return docs_list
    
    def check_web_page(self, source_url: str):
        print("Checking if web page exists in Chroma DB...")
        results = self.db.similarity_search(
            query="",
            filter={"source": source_url},
            k=1
        )
        print(f"Found {len(results)} matching documents for URL: {source_url}")
        return len(results) > 0
    
    def retrieve_docs(self, query: str, url: str, k: int = 5,  acceptable_relevance_score: float=0.5, relevance_score_threshold : float=0.5):
        try:
            print(f"Retrieving top {k} documents for url: {url}")
            mmr_retriever = self.db.as_retriever(search_type="mmr", search_kwargs={"k": k, "filter": {"source": url}})
            results = mmr_retriever.invoke(query)
            print(f"Retrieved {len(results)} documents.")
            
            # Filtering documents based on the relevance score
            print("Acceptable Relevance Score:", acceptable_relevance_score)
            docs_with_scores = []
            top_score = 0
            for doc in results:
                score = self.embed_model.get_relevance_score(query, doc.page_content)
                print(f"DB Document Index: {doc.metadata.get('chunk_index')}, Relevance Score: {score}")
                top_score = max(top_score, score)
                if(score >= acceptable_relevance_score):
                    docs_with_scores.append({
                        "doc": doc,
                        "score": score,
                    })
                
            filtered_results = [
                s["doc"]
                for s in docs_with_scores
                if s["score"] >= relevance_score_threshold * top_score
            ]
            
            print(f"{len(filtered_results)} db documents passed the relevance score threshold of {relevance_score_threshold}.")
            for doc in filtered_results:
                print(f"DB Document Index '{doc.metadata.get('chunk_index')}' passed the threshold.")
            
            return filtered_results
        except Exception as e:
            print("Error retrieving documents:", e)
            return []
