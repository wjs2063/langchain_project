from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from datetime import datetime
from chatbot.domain.entities.utils.time import get_current_time

system_template = """
당신은 AI 도메인 분류 시스템입니다.  
사용자의 **대화 기록과 현재 질문을 종합적으로 분석**하여, 적절한 도메인을 분류하세요.  

"""

user_template = f"""
# 분류 대상 (반드시 4가지 중 하나 선택)
- **wikipedia** : 단어, 인물 등과 관련된 질문
- **weather**: 날씨, 기온, 강수량, 기후, 미세먼지 등과 관련된 질문  
- **schedule**: 일정, 시간표, 약속, 미팅, 예약, 이벤트 등과 관련된 질문  
- **general**: 위 두 범주에 해당하지 않는 일반적인 질문  

---
대화 히스토리 : {{chat_history}}
현재 시각 : {get_current_time(region="kr")}
**추가적인 단어나 설명을 포함하지 마세요.**

---
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        (
            "user",
            f"{user_template}\n\n#Format: {{format_instructions}}\n\n#Question: {{question}}",
        ),
    ]
)
