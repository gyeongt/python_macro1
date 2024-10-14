import cv2
import pytesseract
import pyautogui
import numpy as np
import time
from PIL import Image
import random
import threading
import keyboard
import ctypes

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

black_count = 0
x1, y1 = 627, 215  # 시작
x2, y2 = 960, 620  # 종료 좌표

랜덤_숫자 = random.randint(2, 4)
좌표1 = (1580, 1220)
좌표2 = (1500, 1220)
좌표3 = (1500,190)
좌표4 = (1600,190)
skill_flag = False
# 전역 변수로 사용할 플래그
stop_flag = False
"""
def detect_difference():
    while not stop_flag:
        # 좌표1과 좌표2 사이의 영역 좌표 계산
        x1, y1 = 845, 830
        x2, y2 = 865, 860
        
        # 화면에서 좌표1과 좌표2 사이의 영역 값 캡처
        screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        # 붉은색 여부 확인
        red_threshold = 70  # 붉은 계열의 RGB 값 임계값
        red_count = 0

        # 이미지의 픽셀을 반복하여 붉은색 픽셀 여부 확인
        for y in range(screen.height):
            for x in range(screen.width):
                r, g, b = screen.getpixel((x, y))
                if r > red_threshold and g < red_threshold and b < red_threshold:
                    red_count += 1
        
        if red_count > red_threshold:
            print('skill')
            skill_combo()
        else:
            time.sleep(0.01)

"""
def press_key(key):
    vk_code = ord(key)
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.01)  # 0.01초 대기
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)


def extract_rgb_coordinates(step_size=41.25, threshold_percentage=70):
    x1, y1 = 640, 285  # 시작
    x2, y2 = 970, 615  # 종료 좌표
    global black_count
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save('photo.png')

    # 이미지 읽기
    image = cv2.imread('photo.png')
    print("1")
    # 이미지의 높이와 너비
    height, width = image.shape[:2]
    
    # 알지비 값과 해당 좌표를 저장할 리스트
    result_coordinates = []
    
    # 오른쪽 위부터 왼쪽으로 이동하면서 탐색
    for y in range(0, height, int(step_size)):
        for x in range(width - 1, 0, -int(step_size)):
            # 41.25 픽셀 크기의 영역 추출
            area = image[y:y+int(step_size), x-int(step_size):x]
            print("2")
            # 영역 내의 알지비 값 계산
            unique_colors, counts = np.unique(area.reshape(-1, 3), axis=0, return_counts=True)
            total_pixels = area.shape[0] * area.shape[1]
            print("3")
            # unique_colors와 counts가 비어 있는지 확인
            if len(unique_colors) == 0 or len(counts) == 0:
                print("4")
                print(unique_colors)
                continue
            
            dominant_color_index = np.argmax(counts)
            dominant_color_percentage = counts[dominant_color_index] / total_pixels * 100
            
            # 알지비 값이 threshold_percentage 이상인 경우 좌표와 알지비 값을 저장
            if dominant_color_percentage >= threshold_percentage:
                print("5")
                dominant_color = unique_colors[dominant_color_index]
                result_coordinates.append((dominant_color, (x, y)))
    
    pt1 = pyautogui.locateCenterOnScreen('photo.png')

    for color, coordinate in result_coordinates:
        print("알지비 값:", color, "좌표:", coordinate[0] + x1 - 20, coordinate[1] + y1 + 10)
        pyautogui.mouseDown(pt1[0] - 140, pt1[1] + 190)
        pyautogui.moveTo(coordinate[0] + x1 - 20, coordinate[1] + y1 + 10, duration=2)
        pyautogui.mouseUp()
        time.sleep(2)
    black_count = 0
    # 쓰레드 시작
    thread1 = threading.Thread(target=detect_macro_detector)
    thread3 = threading.Thread(target=번갈아_자동_클릭, args=(좌표1, 좌표2))
    thread1.start()
    thread3.start()


def 번갈아_자동_클릭(좌표1, 좌표2):
    global black_count
    while not stop_flag and black_count == 0:             
        클릭_지연_시간 = random.uniform(0.05, 0.28)           
        for _ in range(랜덤_숫자):
            pyautogui.moveTo(좌표1, duration=0.05)
            x, y = pyautogui.position()
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.moveTo(좌표2, duration=0.05)
            x, y = pyautogui.position()
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            press_key('4')
            press_key('4')

            """    
            pyautogui.moveTo(좌표3, duration=0.05)
            x, y = pyautogui.position()
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.moveTo(좌표4, duration=0.05)
            x, y = pyautogui.position()
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            pyautogui.click(x, y)
            """

# z 키를 누르거나 Ctrl+C를 누르면 작업을 멈추는 함수
def stop_on_z():
    global stop_flag
    print("z 키를 누르면 작업을 멈춥니다.")
    keyboard.wait('z')
    stop_flag = True


def detect_macro_detector():
    global black_count
    while not stop_flag:
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        screenshot.save('photo.png')

        # 이미지 읽기
        image = cv2.imread('photo.png')

        # 이미지를 그레이 스케일로 변환
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 이미지에서 텍스트 인식
        text = pytesseract.image_to_string(gray_image, lang='kor')

        # 인식된 텍스트에 "매크로 검사기"가 포함되어 있는지 확인
        if "검사기" in text:
            print("매크로 검사기를 발견했습니다!")
            black_count = 1
            time.sleep(5)
            extract_rgb_coordinates()
            break
        else:
            print("매크로 검사기를 발견하지 못했습니다.")
            time.sleep(10)

#매크로 감지기 
thread1 = threading.Thread(target=detect_macro_detector)
# z 키를 감지하는 스레드 생성
thread2 = threading.Thread(target=stop_on_z)
#화상키보드의 f와g를 반복하여 누르는 로직
thread3 = threading.Thread(target=번갈아_자동_클릭, args=(좌표1, 좌표2))
#thread4 = threading.Thread(target=detect_difference)

# 스레드 시작
thread1.start()
thread2.start()
thread3.start()
#thread4.start()
# 스레드 종료 대기
thread1.join()
thread2.join()
thread3.join()
#thread4.join()
