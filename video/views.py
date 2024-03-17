import time

import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render


def webcam_view(request):
    return render(request, 'video.html')


def webcam_feed(request):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    def generate_frames():
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            image = cv2.resize(frame, (640, 480))
            _, buffer = cv2.imencode('.jpg', image)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")
