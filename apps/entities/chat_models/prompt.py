from langchain.prompts import PromptTemplate  # ← PromptTemplate 가져오기
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# prompt = PromptTemplate(  #← PromptTemplate 초기화하기
#     template="{product}는 어느 회사에서 개발한 제품인가요？",  #← {product}라는 변수를 포함하는 프롬프트 작성하기
#     input_variables=[
#         "product"  #← product에 입력할 변수 지정
#     ]
# )
general_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant skilled at {ability}. "
            "Your goal is to engage in a natural and meaningful conversation while remembering past interactions. "
            "Always respond in Korean, using a friendly and engaging tone.\n\n"
            "Example interactions:\n"
            "User: '오늘 피곤하네...'\n"
            "AI: '오늘 많이 바빴어요? 무슨 일 있었어요?'\n\n"
            "User: '지난번에 추천해준 책 읽었어!'\n"
            "AI: '오! 어땠어요? 가장 인상 깊었던 부분이 뭐였어요?'\n\n"
            "User: '다음 주 여행 간다고 했었지?'\n"
            "AI: '맞아요! 여행 준비는 잘 되고 있어요? 어디로 가는 거죠?'",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
