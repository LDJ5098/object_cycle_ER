import time
import tkinter as tk
import keyboard
import threading

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
    "1낮": ["01:00 - 늑대"],
    "1밤": ["01:50 - 변이 들개", "01:50 - 변이 멧돼지"],
    "2낮": ["02:20 - 변이 늑대", "02:15 - 늑대", "00:15 - 곰"],
    "2밤": ["01:55 - 변이 들개", "01:55 - 변이 멧돼지", "01:30 - 늑대"],
    "3낮": ["01:55 - 변이 늑대", "01:00 - 곰", "00:45 - 늑대", "00:20 - 변이 닭"],
    "3밤": ["01:40 - 변이 들개", "01:40 - 변이 멧돼지", "01:35 - 변이 곰"],
    "4낮": ["01:20 - 늑대", "00:45 - 곰", "00:30 - 변이 늑대"],
    "4밤": ["01:25 - 변이 닭", "00:25 - 변이 들개", "00:25 - 변이 멧돼지"],
    "5낮": ["01:25 - 늑대", "01:20 - 변이 곰"],
    "5밤": ["01:20 - 곰"],
}

speed_multiplier = 0.1  # 테스트할 때 속도 조절

# 타이머 중지 플래그 및 현재 타이머 스레드
stop_timer = threading.Event()
timer_thread = None

def countdown_timer(name, total_seconds, speed_multiplier=1):
    if name in object_spawn_times:
        objects = object_spawn_times[name]
    else:
        objects = []

    root.title(name)
    label_time.config(text=name)
    root.update()

    # 오브젝트별 레이블 생성
    object_labels = []
    for obj_text in objects:
        label = tk.Label(root, font=('Helvetica', 18, 'bold'), fg='white', bg='black', anchor='nw', justify='left', width=20, text=obj_text)
        label.pack()
        object_labels.append(label)

    current_time = total_seconds

    while current_time >= 0 and not stop_timer.is_set():
        mins, secs = divmod(current_time, 60)

        label_time.config(text=f'{name}: {mins:02d}:{secs:02d}')
        root.update()

        # 시간 일치 여부 확인
        current_time_str = f'{mins:02d}:{secs:02d}'
        for label in object_labels:
            if current_time_str in label.cget("text"):
                label.config(fg='yellow')  # 일치할 때 노란색으로 변경

        time.sleep(1 * speed_multiplier)
        current_time -= 1

    # 타이머 종료 또는 중지 후 레이블 제거
    for label in object_labels:
        label.pack_forget()

def restart_timer(event=None):
    global stop_timer, timer_thread

    if timer_thread and timer_thread.is_alive():
        stop_timer.set()  # 기존 타이머 중지
        timer_thread.join()  # 기존 타이머 스레드가 종료될 때까지 대기

    stop_timer.clear()  # 새로운 타이머 시작

    for child in root.winfo_children():
        if isinstance(child, tk.Label):
            child.pack_forget()

    label_time.config(text="")
    label_time.pack()

    # 새 스레드에서 타이머 실행
    timer_thread = threading.Thread(target=run_timers)
    timer_thread.start()

def run_timers():
    for name, total_seconds in timers:
        if stop_timer.is_set():
            break
        countdown_timer(name, total_seconds, speed_multiplier)

root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)
root.geometry("+10+5")

# Windows 투명도 설정
root.attributes('-transparentcolor', 'black')
root.configure(bg='black')

label_time = tk.Label(root, font=('Helvetica', 20, 'bold'), fg='yellow', bg='black', anchor='nw', justify='left', width=18)
label_time.pack()

# Ctrl + Alt + M 키를 눌렀을 때 restart_timer 함수 호출
keyboard.add_hotkey("ctrl+alt+m", restart_timer)

print('ctrl+alt+m을 누르면 타이머가 작동합니다.\n 게임 시작후 스폰포인트에서 카운트 다운 떨어질 때 작동시키시면 됩니다.')

root.mainloop()