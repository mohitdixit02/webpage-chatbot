from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

class TemplateProvider:
    def __init__(self):
        self.query_type = PromptTemplate(
            template="Act as a classifier. Classify user query as 'casual' if it's a normal talk or 'query' if user is asking for a question.\n Format Instructions {format_instructions}. \n Classify the following query: {query}",
            input_variables=["format_instructions", "query"],
        )
        
        self.casual_talk = PromptTemplate(
            template="You are a Chatbot who answer user queries based on the webpage on which the user is browsing. User has made a casual conversation. Reply to it in following format: {format_instructions} \n. User: {query}",
            input_variables=["format_instructions", "query"],
        )
        
        self.generation_template = PromptTemplate(
            template="You are a Chatbot who answer user queries based on the webpage on which the user is browsing. Use the following context to answer the query. If you don't know the answer, just say that you don't know, don't try to make up an answer. \n Context: {context_docs} \n User Query: {query} \n Reply in the following format: {format_instructions} {behaviour} {search_fail_info}",
            input_variables=["behaviour", "search_fail_info", "format_instructions", "context_docs", "query"],
        )
        
        self.wiki_keywords_template = PromptTemplate(
            template="Act as Keywords Generator. Generate keywords from the user query that can be used to search Wikipedia for relevant articles. User Query: {query}. Follow these instructions: Return minimum 3 keywords as a comma-separated list. Do not return any code, explanation. \n {format_instructions} \n",
            input_variables=["query", "format_instructions"],
        )
        
        self.search_fail_template = PromptTemplate(
            template="You are a Chatbot who answer user queries based on the webpage on which the user is browsing. For some reasons, you are not able to find relevant information. Appologies to the user and ask him to try again with different question. Reply in the following format: {format_instructions}",
            input_variables=["format_instructions"],
        )
        
        self.external_search_fail_apology = "Note: An external search was attempted but failed, so also apologies to the user for the inconvenience."
        self.in_page_search_fail = "Also tell user that no relevant information find from the webpage they are browsing, the output is based on external knowledge."
        self.behv_explain = "Explain the content in more details with subtopic explanations and reasoning. Minimum 800 words."
        self.behv_summary = "Provide a concise summary of the content. Word Limit - 300 words."
        self.behv_oneline = "Provide a one-line reply of the content. Word Limit - 50 words."
        
    def get_query_type_template(self, instructions: str):
        return self.query_type.partial(format_instructions=instructions)
    
    def get_casual_template(self, instructions: str):
        return self.casual_talk.partial(format_instructions=instructions)
    
    def get_wiki_keywords_template(self, instructions: str):
        return self.wiki_keywords_template.partial(format_instructions=instructions)
    
    def get_generation_template(self, instructions: str, behaviour: str="Explain", externalSearchFail: bool=False, inPageSearchFail: bool=False):
        if inPageSearchFail and externalSearchFail:
            return self.search_fail_template.partial(
                format_instructions=instructions
            )
        
        behv_text = ""
        if behaviour == "Explain":
            behv_text = self.behv_explain
        elif behaviour == "Summary":
            behv_text = self.behv_summary
        elif behaviour == "One-Line":
            behv_text = self.behv_oneline
        else:
            behv_text = self.behv_explain
            
        search_fail_text = ""
        if inPageSearchFail:
            search_fail_text = self.in_page_search_fail
        elif externalSearchFail:
            search_fail_text = self.external_search_fail_apology
        
        return self.generation_template.partial(
            behaviour=behv_text,
            search_fail_info=search_fail_text,
            format_instructions=instructions
        )