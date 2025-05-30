from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""문장을 바탕으로 질문에 답하세요.

문장: 
{document}

질문: {query}
""",
    input_variables=["document", "query"],
)


