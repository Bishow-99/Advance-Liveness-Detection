import cv2
from calculate_coordinate.measurement import blink_ratio, landmarks_detection, mouth_open_ratio, face_direction_identification
import numpy as np
import mediapipe as mp
 

frame_counter = 0
closed_eye_counter = 0
open_mouth_counter = 0
total_blinkS = 0
number_of_times_mouth_opened = 0
BLINK_THRESHOLD=5.5
FRAME_THRESHOLD = 3

map_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)



fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_liveness2.mp4', fourcc, 20, (640,  480))
with map_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_faces=1
    ) as face_mesh:

   while cap.isOpened():
        frame_counter+=1
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frame.flags.writeable = False
        results = face_mesh.process(rgb_frame)
        
        frame.flags.writeable = True
        if results.multi_face_landmarks:
            mesh_coords = landmarks_detection(frame, results, False)
            # cv2.polylines(frame, [np.array([mesh_coords[p] for p in LEFT_EYE], dtype=np.int32)],  True, (0, 0, 255), 2)
            # cv2.polylines(frame, [np.array([mesh_coords[p] for p in RIGHT_EYE], dtype=np.int32)],  True, (0, 0, 255), 2)
            total_ratio = blink_ratio(frame, mesh_coords)
            if total_ratio > BLINK_THRESHOLD:
                closed_eye_counter+=1
            else:
                if closed_eye_counter>FRAME_THRESHOLD:
                    total_blinkS += 1
                    closed_eye_counter = 0
                    if total_blinkS > 5:
                        print("You have blinked the eyes nicely")
                    else:
                        continue
            mouth_ratio = int(mouth_open_ratio(frame, mesh_coords))
            if mouth_ratio>40:
                open_mouth_counter+=1
            else:
                if open_mouth_counter>FRAME_THRESHOLD:
                    number_of_times_mouth_opened+=1
                    open_mouth_counter = 0
                    if number_of_times_mouth_opened>3:
                        print("Mouth opened task is complete")
                    else:
                        continue
           
            cv2.putText(frame, f"Eyes Blinked:{total_blinkS}", (390, 33), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Mouth Opened:{number_of_times_mouth_opened}", (366, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 50, 255), 2, cv2.LINE_AA)
        x, y, z = face_direction_identification(frame, results)

        if y < -16:
            output = "Right"
        elif y>16:
            output = "Left"
        elif x<-16:
            output = "Down"
        elif x>16:
            output = "UP"
        else:
            output = "Forward"
        cv2.putText(frame, f"Face Direction {output}", (230, 475), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        out.write(frame)
        cv2.imshow("image", frame)
        if cv2.waitKey(1) & 0XFF==27:
            break
cap.release()
out.release()
cv2.destroyAllWindows()


