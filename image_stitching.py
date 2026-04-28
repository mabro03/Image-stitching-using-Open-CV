import numpy as np
import cv2 as cv

def preprocess_image(img, target_height):
    h, w = img.shape[:2]
    if h != target_height:
        target_width = int(w * (target_height / h))
        img = cv.resize(img, (target_width, target_height), interpolation=cv.INTER_AREA)
    return img

def stitch_with_roi(base_img, next_img):
    h_base, w_base = base_img.shape[:2]
    h_next, w_next = next_img.shape[:2]

    roi_x_start = w_base // 2 
    base_roi = base_img[:, roi_x_start:]

    fdetector = cv.BRISK_create()
    kp1, des1 = fdetector.detectAndCompute(base_roi, None)
    kp2, des2 = fdetector.detectAndCompute(next_img, None)

    for i in range(len(kp1)):
        old_pt = kp1[i].pt
        kp1[i].pt = (old_pt[0] + roi_x_start, old_pt[1])

    fmatcher = cv.DescriptorMatcher_create('BruteForce-Hamming')
    matches = fmatcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    pts1 = np.array([kp1[m.queryIdx].pt for m in matches], dtype=np.float32)
    pts2 = np.array([kp2[m.trainIdx].pt for m in matches], dtype=np.float32)

    H, mask = cv.findHomography(pts2, pts1, cv.RANSAC, 3.0)

    corners_next = np.array([[0, 0], [0, h_next], [w_next, h_next], [w_next, 0]], dtype='float32').reshape(-1, 1, 2)
    warped_corners = cv.perspectiveTransform(corners_next, H)
    max_x = int(max(np.max(warped_corners[:, :, 0]), w_base))
    
    img_merged = cv.warpPerspective(next_img, H, (max_x, h_base))
    
    res = img_merged.copy()
    res[0:h_base, 0:w_base] = base_img
    
    return res

img1 = cv.imread('image_01.jpg')
img2 = cv.imread('image_02.jpg')
img3 = cv.imread('image_03.jpg')

if img1 is None or img2 is None or img3 is None:
    exit()

th = img1.shape[0]
img2 = preprocess_image(img2, th)
img3 = preprocess_image(img3, th)

res12 = stitch_with_roi(img1, img2)
final_res = stitch_with_roi(res12, img3)

cv.imshow('Final Result', cv.resize(final_res, (0,0), fx=0.5, fy=0.5))
cv.waitKey(0)
cv.destroyAllWindows()