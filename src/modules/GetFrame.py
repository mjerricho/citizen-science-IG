import sys

import cv2


class GetFrame:
    def __init__(self, video_file: str) -> None:
        print("initialising GetFrame")
        self.video_file = video_file
        self.cap = cv2.VideoCapture(self.video_file)

    def get_frame(self, frame_number: int):
        print("getting the frame of the video ")
        # can include the computer vision otter detector here
        ret, frame = self.cap.read()
        if ret:
            return frame
        print("failed")
        sys.exit()

    def save_image(self, frame):
        print("Image saved")
        cv2.imwrite("screenshot.jpg", frame)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


# get_frame = GetFrame(sys.argv[1])
# frame = get_frame.get_frame(1)
# get_frame.save_image(frame)
# get_frame.release()
