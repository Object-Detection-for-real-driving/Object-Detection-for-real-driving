from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2

con= [0.2]


CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("testModel/MobileNetSSD_deploy.prototxt.txt",
								 "testModel/MobileNetSSD_deploy.caffemodel")
					


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)


fps = FPS().start()


while True:
    frame = vs.read()

    frame = imutils.resize(frame, width=640, height=480)

    (h, w) = frame.shape[:2]
    resized_image = cv2.resize(frame, (300, 300))

    blob = cv2.dnn.blobFromImage(resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)


    net.setInput(blob)

    predictions = net.forward()
    print("pre : ", predictions)
    print("pre : ", predictions.shape)

    for i in np.arange(0, predictions.shape[2]):
        confidence = predictions[0, 0, i, 2]

        if confidence > con:
            idx = int(predictions[0, 0, i, 1])
            print("pre: ", predictions[0, 0, i, 3:7])
            print("pre.shape: ", predictions[0, 0, i, 3:7].shape)

            box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("Object detected: ", label)

            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15

            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

fps.stop()

print("[INFO] Elapsed Time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approximate FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()