from langchain_core.prompts import PromptTemplate
from langchain.prompts import PromptTemplate


general_prompt = PromptTemplate.from_template(
    template="""
당신은 친절하고 유능한 AI 비서입니다.  
사용자의 질문을 이해하고 명확하면서도 유용한 답변을 제공하세요.  
가능하면 간결하게 대답하되, 필요한 경우 추가 정보를 제공하세요.  
이전 대화 내용을 고려하여 일관된 답변을 유지하세요.

📝 대화 기록:
{chat_history}

🙋 사용자: {question}
🤖 AI:"""
)
