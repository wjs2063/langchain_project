# country_server.py
from mcp.server.fastmcp import FastMCP

# 간단한 "국가-수도" 데이터베이스 (딕셔너리)
capitals = {
    "대한민국": "서울",
    "United States": "Washington, D.C.",
    "France": "Paris",
    "Japan": "Tokyo",
}

# MCP 서버 생성
mcp = FastMCP("CountryInfo")


# 1. Resource 정의: 모든 국가 리스트 제공
@mcp.resource("country://list")
def list_countries() -> list[str]:
    """사용 가능한 모든 국가 이름 리스트 반환"""
    return list(capitals.keys())


# 2. Tool 정의: 특정 국가의 수도 조회
@mcp.tool()
def get_capital(country: str) -> str:
    """주어진 국가의 수도 이름을 반환"""
    return capitals.get(country, "Unknown")


# 서버 실행
if __name__ == "__main__":
    mcp.run()
