from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

prompt = PromptTemplate(
    template=f"""
    You are a professional AI assistant.  
Answer the user's question based on the information retrieved from Wikipedia.  
Your response should be in Korean, even though the retrieved information is in English.  
If the information is insufficient, respond with: "추가 정보가 필요합니다."  

**user_information**
{{user_info}}

User Question: {{question}}  
Wikipedia Search Result (in English): {{context}}  

---  
🔹 Final Answer (in Korean):
""",
    input_variables=["context", "question"],
)
