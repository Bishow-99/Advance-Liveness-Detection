# Liveness-Detection
The main aim of liveness detection is to confirm that the biometric data comes from a real person and not from a fake image, video, mask, or any other trickery.

# Demo
https://github.com/Bishow-99/Liveness-Detection/assets/80660041/72c572a6-f638-43b0-9bb1-807e9c74ca5a

# How does it Work?
Here are the steps to find the living person in the frame:

(i) Utilize Google's MediaPipe package to locate key points on a person's face.

(ii) Analyze these points to measure changes in the distance between specific landmarks, such as the corners of the eyes. When the distance between these points becomes smaller, 
it suggests that the person is blinking their eyes.

(ii) Moreover, this repository covers one of the important topics which is camera calibration, which is used to find the head position of the person.

# Camera Calibration 3D to 2D transformation
In order to find the position of the face or head we need to understand how camera calibration works.

Camera Calibration is the process of transforming 3D world coordinates into 2D image coordinates. It involves establishing relationships between the camera's internal parameter(intrinsic) and
position and orientation in the world that is called extrinsic parameters.
(1) Intrinsic Parameters: Intrinsic parameter relate to the internal characteristics of the camera that includes:
     (a) Focal Length: The focal length of the camera determines the distance between the lens and image sensor or it indicates how much the camera can zoom in and zoom out.
     (b) Principal Point(c_x, c_y): The coordinates of the optical center which is the point where the optical axis(imaginary line that passes from the camera's lens through it's center to the image sensor.
     (c) Lens Distortion: The camera may introduce radial distortion which can cause straight lines to appear as curved.


(2) Extrinsic Parameters: It defines the camera position and orientation in the real world, that c

