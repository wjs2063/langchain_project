from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


weather_template = f"""
사용자의 질문에서 **가장 구체적인 위치 정보**를 추출해.  
예를 들어, "서울 날씨 어때?"라면 "서울", "강남구 날씨 알려줘"라면 "서울 강남구"를 반환해.  
가능하면 **시, 구, 동까지 포함**하고, 특정 지역이 없으면 "위치를 확인할 수 없음"이라고 답해. 

**기본정보**
현재 날짜 정보 : {{user_info}}

**필수 규칙**
대답은 모두 한국어로 반환

**변환규칙**
mist -> 안개
rainy -> 비
snow -> 눈
clear sky -> 화창함
등 모두 한글로 번역해서 전달해줘

"""


weather_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"{weather_template}",
        ),
        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
