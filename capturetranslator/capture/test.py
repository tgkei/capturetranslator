import cv2
import numpy as np
import pyautogui

refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    global refPt, cropping
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


if __name__ == "__main__":
    myScreenshot = pyautogui.screenshot()
    image = np.array(myScreenshot)

    # load the image, clone it, and setup the mouse callback function
    clone = image.copy()
    cv2.namedWindow("image")
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

    # close all open windows
    cv2.destroyAllWindows()
