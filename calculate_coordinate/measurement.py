import cv2
import math
import numpy as np

LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 




def landmarks_detection(img, results, draw=False):
    img_height, img_width = img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height))
                  for point in results.multi_face_landmarks[0].landmark]
    # cv2.polylines(img, [np.array([mesh_coord[p] for p in LEFT_EYE], dtype=np.int32)],  True, (0, 0, 255), 2)
    # cv2.polylines(img, [np.array([mesh_coord[p] for p in RIGHT_EYE], dtype=np.int32)],  True, (0, 0, 255), 2)
    
    return mesh_coord

def euclideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance

def blink_ratio(img, landmarks):

        #Right EYE
    #right horizontal
    rh_right = landmarks[RIGHT_EYE[0]]
    rh_left = landmarks[RIGHT_EYE[8]]

    #right vertical
    rv_top = landmarks[RIGHT_EYE[12]]
    rv_bottom = landmarks[RIGHT_EYE[4]]

    # cv2.line(img, rh_right, rh_left, (0, 255, 0), 2)
    # cv2.line(img, rv_top, rv_bottom, (0, 0, 0), 2)

        #LEFT_EYE
    # horizontal line
    lh_right = landmarks[LEFT_EYE[0]]
    lh_left = landmarks[LEFT_EYE[8]]

    # vertical line
    lv_top = landmarks[LEFT_EYE[12]]
    lv_bottom = landmarks[LEFT_EYE[4]]

    # cv2.line(img, lh_right, lh_left, (0, 255, 0), 2)
    # cv2.line(img, lv_top, lv_bottom, (0, 0, 0), 2)

    rh_distance = euclideanDistance(rh_right, rh_left)
    rv_distance = euclideanDistance(rv_top, rv_bottom)

    lh_distance = euclideanDistance(lh_right, lh_left)
    lv_distance = euclideanDistance(lv_top, lv_bottom)

    r_ratio = rh_distance/rv_distance
    l_ratio = lh_distance/lv_distance

    total_ratio = (r_ratio+l_ratio)/2
    return total_ratio


def mouth_open_ratio(img, landmarks):
    top_left_lips = landmarks[LIPS[24]]
    top_right_lips = landmarks[LIPS[26]]
    bottom_left_lips = landmarks[LIPS[17]]
    bottom_right_lips = landmarks[LIPS[6]]
    left_vertical_distance = euclideanDistance(top_left_lips, bottom_left_lips)
    right_vertical_distance = euclideanDistance(top_right_lips, bottom_right_lips)
    mouth_ratio = (left_vertical_distance+right_vertical_distance)/2
    # cv2.line(img, top_left_lips, bottom_left_lips, (0, 255, 0), 2)
    # cv2.line(img, top_left_lips, bottom_left_lips, (0, 255, 0), 2)
    # cv2.line(img, top_right_lips, bottom_right_lips, (0, 0, 0), 2)
    # cv2.line(img, top_left_lips, bottom_left_lips, (0, 255, 0), 2)
    # cv2.polylines(img, [np.array([top_left_lips, bottom_left_lips, bottom_right_lips, top_right_lips], dtype = np.int32)], True, (0, 0, 255), 2 )
    return mouth_ratio



def face_direction_identification(frame, results):
    img_h, img_w, _ = frame.shape
    face_3d = []
    face_2d = []
    for face_landmarks in results.multi_face_landmarks:
        if face_landmarks is None:
            continue
        for idx, lm in enumerate(face_landmarks.landmark):
            if idx == 33 or idx==263 or idx==1 or idx==61 or idx==291 or idx==199:
                x, y, z = int(lm.x*img_w), int(lm.y*img_h), lm.z
                face_2d.append([x, y])
                face_3d.append([x, y, z])
        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)
        focal_length = 1*img_w
        cam_matrix = np.array([[focal_length, 0, img_w/2],
                                [0, focal_length, img_h/2],
                                [0, 0, 1]] )       
        dist_matrix = np.zeros((4,1), dtype=np.float64)
    
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        rot_mat, jacobian_mat = cv2.Rodrigues(rot_vec)
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rot_mat)
        x = angles[0]*360
        y = angles[1]*360
        z = angles[2]*360
        return x, y, z