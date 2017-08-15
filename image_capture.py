import io
import cv2

class ImageCapture:

    index = 1

    def capture_image(self):
        vCapture = cv2.VideoCapture(0)

        frameIsAvailable, frame = vCapture.read()
        key = cv2.waitKey(1)
        while frameIsAvailable and key != 27:
            cv2.imshow("Press esc to take picture", frame)
            frameIsAvailable, frame = vCapture.read()
            key = cv2.waitKey(1)
        vCapture.release()
        cv2.destroyWindow("Press esc to take picture")
        imgFileName = "savedImage%s.jpg" % (ImageCapture.index)
        print(imgFileName)
        ImageCapture.index += 1
        cv2.imwrite(imgFileName, frame)
        return imgFileName