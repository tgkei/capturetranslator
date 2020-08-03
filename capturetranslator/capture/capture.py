import pytesseract
import cv2
import numpy as np
import pyautogui


class Capture(object):
    refPt = []
    cropping = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Capture, cls).__new__(cls)
        return cls.instance

    @classmethod
    def to_str(cls):
        # callback function
        def click_and_crop(event, x, y, flags, param):
            # if the left mouse button was clicked, record the starting
            # (x, y) coordinates and indicate that cropping is being
            # performed
            if event == cv2.EVENT_LBUTTONDOWN:
                assert cropping == False, "Cropping should be False before mouse click"
                refPt = [(x, y)]
                cropping = True

            # check to see if the left mouse button was released
            elif event == cv2.EVENT_LBUTTONUP and cropping:
                # record the ending (x, y) coordinates and indicate that
                # the cropping operation is finished
                refPt.append((x, y))
                cropping = False
                # draw a rectangle around the region of interest
                assert len(refPt) == 2, "Coordinates are not correctly corrected"
                # return refPt
                cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
                cv2.imshow("image", image)

        myScreenshot = pyautogui.screenshot()
        image = np.array(myScreenshot)
        # load the image, clone it, and setup the mouse callback function
        clone = image.copy()

        # create cv2 window and locate on 0, 0
        cv2.namedWindow("image")
        cv2.moveWindow("image", 0, 0)
        cv2.setMouseCallback("image", click_and_crop)

        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF
            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image = clone.copy()
            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                break
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        if len(refPt) == 2:
            roi = clone[refPt[0][1] : refPt[1][1], refPt[0][0] : refPt[1][0]]
            cv2.imshow("ROI", roi)
            cv2.waitKey(0)

        # gray scale and preprocessing image to improve ocr
        gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
        gray, img_bin = cv2.threshold(
            gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )
        gray = cv2.bitwise_not(img_bin)
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(gray, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        out_below = pytesseract.image_to_string(img)

        print(out_below)
        # close all open windows
        cv2.destroyAllWindows()
