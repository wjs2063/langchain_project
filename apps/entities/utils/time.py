from datetime import datetime, timezone, timedelta


def get_current_time(region="kr") -> tuple:
    """
    시간, 요일을 반환하는 함수
    """
    week_day = {
        0: "월요일",
        1: "화요일",
        2: "수요일",
        3: "목요일",
        4: "금요일",
        5: "토요일",
        6: "일요일",
    }

    user_time_zone = timezone(timedelta(hours=+9))
    if region == "en":
        user_time_zone = timezone(timedelta(hours=-9))
    _current_time = datetime.now(user_time_zone)
    _week_day = week_day[_current_time.weekday()]

    return _current_time.strftime("%Y-%m-%d %H:%M:%S"), _week_day


# print(get_current_time(region="en"))
