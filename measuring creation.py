import time

# 타이머 데이터 (각 시간대의 총 시간)
timers = [
    ("1낮", 2*60 + 30),
    ("1밤", 1*60 + 50),
    ("2낮", 2*60 + 20),
    ("2밤", 2*60),
    ("3낮", 2*60 + 20),
    ("3밤", 2*60),
    ("4낮", 2*60),
    ("4밤", 1*60 + 40),
    ("5낮", 1*60 + 30),
    ("5밤", 1*60 + 20),
]

# 오브젝트 생성 시간 (각 시간대와 해당 시간 및 오브젝트)
object_spawn_times = {
    "1낮": {1*60+0: "늑대"}, # 1:30까지 늑대 생성
    "1밤": {1*60+50: "곰", 1*60+50: "변이 닭", 1*60+50: "변이 들개, 변이 멧돼지"}, # 1:50까지 곰 생성
    "2낮": {2*60+15: "늑대", 0*60+15: "곰", 2*60+20 : "변이 늑대"}, # 2:15까지 늑대 생성
    "2밤": {1*60+30: "늑대", 2*60+15: "변이 닭", 1*60+55: "변이 들개, 변이 멧돼지", 2*60+20: "변이 곰"}, # 2:00까지는 없음
    "3낮": {0*60+45: "늑대", 1*60+0: "곰", 0*60+20:"변이 닭", 1*60+55:"변이 늑대"},  # 1:15까지 늑대 생성, 2:20까지 곰 생성
    "3밤": {1*60+40: "변이 들개, 변이 멧돼지", 1*60+35: "변이 곰"}, # 2:00까지는 없음
    "4낮": {1*60+20: "늑대", 0*60+45: "곰", 0*60+30:"변이 늑대"}, # 1:40까지 늑대 생성
    "4밤": {1*60+25: "변이 닭", 0*60+25:"변이 들개, 변이 멧돼지"}, # 1:45까지 곰 생성
    "5낮": {1*60+25: "늑대", 1*60+20:"변이 곰"},      # 1:35까지 늑대 생성
    "5밤": {1*60+20: "곰"}, # 1:40까지 곰 생성
}

def countdown_timer(name, total_seconds, spawn_times, speed_multiplier=1):
    current_time = total_seconds
    while current_time >= 0:
        mins, secs = divmod(current_time, 60)
        timer = f'{name}: {mins:02d}:{secs:02d}'
        
        # 스폰 시간이 10초 이하로 남았을 때 안내 메시지 출력
        for spawn_time in spawn_times:
            if current_time == spawn_time:
                print(f'{name} {mins:02d}:{secs:02d} - {spawn_times[spawn_time]}')

        time.sleep(1 * speed_multiplier)
        current_time -= 1

    print(f'------------------')

# 테스트할 때 속도 조절 0.01 = 100배 빠름
speed_multiplier = 0.01

for name, total_seconds in timers:
    spawn_times = object_spawn_times.get(name, {})
    countdown_timer(name, total_seconds, spawn_times, speed_multiplier)
