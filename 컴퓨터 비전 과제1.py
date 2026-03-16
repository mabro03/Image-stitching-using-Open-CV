import cv2

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0
out = cv2.VideoWriter('output.avi', fourcc, fps, (640, 480)) # 저장할 파일 이름, 코덱, 프레임 속도, 해상도

record = False  # 초기 모드: Preview

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Record 모드일 때만 저장
    if record:
        out.write(frame)
        # 화면에 빨간 원 표시
        cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)

    cv2.imshow('Video Recorder', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == 32:  # Space 키로 일시정지와 재생모드 전환
        record = not record 
    elif key == ord('2'):
        fps = 20.0
        out = cv2.VideoWriter('output.avi', fourcc, fps, (640, 480))
    elif key == ord('3'):
        fps = 30.0
        out = cv2.VideoWriter('output.avi', fourcc, fps, (640, 480))

cap.release()
out.release()
cv2.destroyAllWindows()
