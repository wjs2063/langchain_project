# langchain_project
LangChain Project


## 기능  
1. 일반 대화 챗봇  
2. 날씨조회(geopy)  
3. 스케쥴 관리 Agent (\w google calendar 등록,조회)   
4. 외부 검색엔진 연동( tavily, 네이버 백과사전, wikipedia)  


## 구조 
apis : api endpoit 관리  
entity : domain 별 각 entity 집합  
service : 서비스계층의 비즈니스로직   
infra : 외부 기술(DB,celery 등 외부 기술적요소들의 집합)  
exception : 예외처리   


## 동작 흐름 
**비순환 구조** 
apis -> service  -> entity | infra 




[시연영상]

https://github.com/user-attachments/assets/021556b4-4e7e-4335-a384-f6e3f9ba681b




# USAGE

```

docker compose -f builds/compose.yml up -d

poetry install

uvicorn main:app --host=0.0.0.0 --port=8000
```

