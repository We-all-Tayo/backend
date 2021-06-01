우리 모두 타요
===

건국대학교 컴퓨터공학과 2021년 1학기 졸업 프로젝트 1조 [We All TAYO](https://github.com/We-all-Tayo/we_all_tayo) 팀의 백엔드 서버

프로젝트 구조
---

```
.
├── app.py
├── checkpoints/ # YOLOv4 라이브러리 (not in repo)
├── config.py # 앱 구성 파일 (not in repo)
├── service/
│   ├── angle_detection.py # 허프 변환을 통해 버스 경계선을 찾아 측면 각도 계산
│   ├── bus_arrive.py # 공공API를 통해 현재 버스 정류장에 대한 곧 도착 버스 목록 확인
│   ├── calculate_distance_angle.py # 주어진 좌표와 측면 각도를 통해 버스 출입문 거리 및 각도 계산
│   ├── color_detection.py # 주어진 이미지의 색상 분석을 통해 버스 타입 유추
│   ├── core/ # Tensorflow YOLOv4 core 라이브러리
│   ├── data/ # YOLOv4 훈련 데이터 (not in repo)
│   ├── door_detection.py # 버스 출입문 위치 추정
│   ├── number_detection.py # 버스 노선번호 추정
│   ├── utils.py # 부가적인 유틸리티 함수
│   ├── __init__.py
│   └── yolo.py # YOLOv4를 통해 버스 인식
└── view/
    └── __init__.py
```

의존성
---

```bash
$ pip3 install easydict numpy==1.19.2 opencv-python pytesseract tensorflow==2.4.1 urllib3 flask flask_cors
```

- [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract)


```bash
$ sudo apt install tesseract-ocr-kor
$ export TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"
$ # 이는 Ubuntu 20.04 기준이며, 운영체제에 따라 차이가 있을 수 있습니다.
```
