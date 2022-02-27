from flask import Flask, render_template, Response
import cv2

# from gevent import pywsgi


class VideoCamera1(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        # self.video = cv2.VideoCapture("rtsp地址") 
        #此处为自己的视频流url 格式 "rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, channel)
        # self.video=cv2.VideoCapture('rtsp://admin:123456@192.168.1.64//Streaming/Channels/101')
        
        # self.video=cv2.VideoCapture('rtsp://admin:Admin123@10.122.21.68//Streaming/Channels/101')
        # self.video=cv2.VideoCapture('rtsp://admin:jky12345@10.122.21.68//Streaming/Channels/101')
        self.video = cv2.VideoCapture(0) 
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera2(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        # self.video = cv2.VideoCapture("rtsp地址") 
        #此处为自己的视频流url 格式 "rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, channel)
        # self.video=cv2.VideoCapture('rtsp://admin:123456@192.168.1.64//Streaming/Channels/101')
        
        # self.video=cv2.VideoCapture('rtsp://admin:Admin123@10.122.21.68//Streaming/Channels/101')
        # self.video=cv2.VideoCapture('rtsp://admin:jky12345@10.122.21.68//Streaming/Channels/101')
        self.video = cv2.VideoCapture(1) 
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

app = Flask(__name__)


def index():
    # jinja2模板，具体格式保存在index.html文件中
    # return render_template('index.html')
    return render_template('html_video.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# def gen2(camera):
#     while True:
#         frame = camera.get_frame2()
#         # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed1')  # 这个地址返回视频流响应
def video_feed1():
    return Response(gen(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')   
@app.route('/video_feed2')  # 这个地址返回视频流响应
def video_feed2():
        return Response(gen(VideoCamera2()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 

    # 访问地址： http://localhost:5000/video_feed
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000),app)
    # server.serve_forever() 

