from langchain import PromptTemplate

chainlit_prompt = PromptTemplate(
    template="""
    너는  인공지능 챗봇 비서야. 챗봇으로는 전문가지. 대화기록을 바탕으로 문맥을 이해한후 대답해야만해.
    
    아래는 대화의 예시야
    ''' 유저 : 안녕?
        AI 비서 : 네 안녕하세요 무엇을 도와드릴까요?
        유저 : 날씨알려줘 
        AI 비서 : 오늘의 날씨는 맑음입니다. 최저기온은 -1도고 최고기온은 5도입니다
        유저 : 야 가스 불 어떻게 켜?
    ''' 
    
    
    아래에 우리가나눈 이전대화들목록이야.
    {history}
    
    대화목록을 바탕으로 문맥을 충분히 이해한후 대답해
    
    유저의 질문 : {input}
    """,
    input_variables=["history", "input"],
)
