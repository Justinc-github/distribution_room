import cv2
from django.http import StreamingHttpResponse


#  将生成器函数定义在视图函数外部
def video_frame_generator(ip, user, password):
    cap = cv2.VideoCapture("rtsp://" + user + ":" + password + "@" + ip + ":554/h264/ch1/main/av_stream")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type:  image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    finally:
        cap.release()


def video_feed(request):
    #  摄像头配置
    ip = '192.168.1.64'
    user = 'admin'
    password = 'yu20021014..'

    #  返回流响应
    return StreamingHttpResponse(video_frame_generator(ip, user, password),
                                 content_type="multipart/x-mixed-replace;boundary=frame")