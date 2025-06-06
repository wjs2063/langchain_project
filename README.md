# langchain_project
LangChain Project


## 기능  
1. 일반 대화 챗봇  
2. 날씨조회(geopy)  
3. 스케쥴 관리 Agent (\w google calendar 등록,조회)   
4. 외부 검색엔진 연동( tavily, 네이버 백과사전, wikipedia)  


## 구조 
application : 유스케이스들의 집합  
domain : domain별 각 entity 집합     
infra : 외부 기술(DB,celery 등 외부 기술적요소들의 집합)  
presentation : rest,grpc 등 api 정의  
exception : 예외처리     


## 동작 흐름 
**비순환 구조** 
presentation -> appliation -> domain | infra

## 서버 아키텍쳐

![image](https://github.com/user-attachments/assets/2c427d15-1ee9-46c8-bc27-3924282b067b)



## Chain 동작 흐름 

![image](https://github.com/user-attachments/assets/a33cb157-15ec-4f0a-84ff-3eeb2a281033)




[시연영상]




https://github.com/user-attachments/assets/c1c945c3-02c0-4d92-a061-ed311fc390ba





# USAGE

```

docker compose -f builds/compose.yml up -d

poetry install

uvicorn main:app --host=0.0.0.0 --port=8000
```

