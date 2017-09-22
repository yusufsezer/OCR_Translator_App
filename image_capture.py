import cv2


class ImageCapture:
    """Handles webcam access and image capture.

    :type index: int
    :var index: index to prevent saving files with the same name as already-saved files.
    """

    index = 1

    def capture_image(self) -> str:
        """Launches webcam window, allows user to capture image, and saves the image as a .jpg file."

        :return: the file name of the captured/saved image.
        """
        v_capture = cv2.VideoCapture(0)

        frame_is_available, frame = v_capture.read()

        key = cv2.waitKey(1)
        while frame_is_available and key != 27:
            cv2.imshow("Press esc to take picture", frame)
            frame_is_available, frame = v_capture.read()
            key = cv2.waitKey(1)
        v_capture.release()
        cv2.destroyWindow("Press esc to take picture")

        img_file_name = "savedImage%s.jpg" % (ImageCapture.index)
        ImageCapture.index += 1
        cv2.imwrite(img_file_name, frame)

        return img_file_name
