import time
import cv2

def video_show(frame,now_time,winName):
    cv2.putText(frame, "time {time}".format(time=now_time), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(winName, frame)


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    fps=cam.get(cv2.CAP_PROP_FPS)
    frame_q=[]
    #延时的帧数
    max_frame=60

    while True:
        frame_dict={}
        ret, frame = cam.read()
        time1 = time.strftime('%H:%M:%S', time.localtime())
        #正常播放
        video_show(frame,time1,'camera_now')

        #按帧存储
        frame_dict['time']=time1
        frame_dict['frame']=frame

        if len(frame_q)<max_frame:
            frame_q.append(frame_dict)
        if len(frame_q)>max_frame-1:
            data=frame_q[0]
            frame=data['frame']
            now_time=data['time'] 
            #延时播放
            video_show(frame, now_time, 'camera_old')
            del frame_q[0]

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()