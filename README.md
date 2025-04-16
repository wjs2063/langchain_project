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




# Feature

- 매번 로그를 찍는 과정이 코드레벨에서 품질이 저하되므로 데코레이터로 제작  
- required : ``` pip install python-json-logger ```
- source : ```apps/infras/utils/loggings/decorator.py```

### Explanation
- before = True -> input 기록
- after = True -> output 기록 
- class & func name 기록 


log trace example 
```

@trace(logger=logger,before=True,after=True)
async def ainvoke(self, message: str):
    request_information = {
        "question": message,
        "ability": "chatting",
        "chat_history": history,
        "user_info": get_current_time(region="kr"),
    }
    return request_information
   
```
