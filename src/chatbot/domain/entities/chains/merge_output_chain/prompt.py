from langchain_core.prompts import PromptTemplate


template = """
당신은 정보 요약 및 정리 전문가입니다.  
사용자의 질문을 작은 질문으로 나누어 도메인별 전문가에게 질문을 던졌고, 그들의 답변을 수집했습니다.  
이제 이 정보를 바탕으로 사용자가 이해하기 쉽게 하나의 응답을 만들어 주세요.

### 사용자의 원래 질문:
{question}

### 도메인별 응답:
{domain_answers}

### 응답을 생성할 때 참고할 사항:
- 모든 도메인별 응답을 종합하여 일관된 하나의 답변을 제공하세요.
- 답변이 자연스럽고 논리적이어야 합니다.
- 필요하면 응답의 순서를 정리하여 가독성을 높이세요.
- 추가적인 정보가 필요한 경우, 명확하게 그 부분을 언급하세요.

### 최종 응답:
"""
merge_output_prompt = PromptTemplate.from_template(template=template)
