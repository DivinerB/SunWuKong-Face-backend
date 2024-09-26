import cv2
import dlib
import numpy as np

def face_swap(file_path):

    sun_wukong_image = cv2.imread("SUNWUKONG.png")
    your_face_image = cv2.imread(file_path)
    sun_wukong_face_mask = cv2.cvtColor(cv2.imread("sun_wukong_face_mask.png"), cv2.COLOR_BGR2GRAY)

    x, y, w, h = 145, 190, 200, 200
    sun_wukong_face_image = sun_wukong_image[y: y + h, x: x + w, ]
    result = sun_wukong_image
    gray_your_face = cv2.cvtColor(your_face_image, cv2.COLOR_BGR2GRAY)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    your_face_faces = detector(gray_your_face)
    if len(your_face_faces) < 1:
        return "result_uploads/SUNWUKONG.png"
    your_landmarks = predictor(gray_your_face, your_face_faces[0])

    mask = np.zeros_like(gray_your_face)
    xmax = 0
    ymax = 0
    xmin, ymin = mask.shape

    for i in range(30, 68):
        x_part = your_landmarks.part(i).x
        y_part = your_landmarks.part(i).y
        xmax = max(xmax, x_part)
        ymax = max(ymax, y_part)
        xmin = min(xmin, x_part)
        ymin = min(ymin, y_part)
        
    pw = xmax - xmin
    ph = ymax - ymin
    center = (w // 2, h // 2)

    part_image = your_face_image[ymin - (int)(0.38 * ph): ymax + (int)(0.16 * ph), xmin - (int)(0.3 * pw): xmax + (int)(0.22 * pw), ]
    your_face_resized = cv2.resize(part_image, (w, h))

    composite_image = cv2.seamlessClone(your_face_resized, sun_wukong_face_image, sun_wukong_face_mask, center, cv2.NORMAL_CLONE)

    result[y: y + h, x: x + w, ] = composite_image
    new_file_path = "result_" + file_path
    cv2.imwrite(new_file_path, result)

    return new_file_path