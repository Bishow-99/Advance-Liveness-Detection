# Liveness-Detection
The main aim of liveness detection is to confirm that the biometric data comes from a real person and not from a fake image, video, mask, or any other trickery.

# Demo
https://github.com/Bishow-99/Liveness-Detection/assets/80660041/72c572a6-f638-43b0-9bb1-807e9c74ca5a

# How does it Works?
Here are the steps to find the living person in the frame:

(i) Utilize Google's MediaPipe package to locate key points on a person's face.

(ii) Analyze these points to measure changes in the distance between specific landmarks, such as the corners of the eyes. When the distance between these points becomes smaller, 
it suggests that the person is blinking their eyes.

(ii) Moreover, this repository covers one of the important topics which is camera calibration, which is used to find the head position of the person.

# Camera Calibration 3D to 2D Transformation
In order to find the position of the face or head we need to understand how camera calibration works.

Camera Calibration is the process of transforming 3D world coordinates into 2D image coordinates. It involves establishing relationships between the camera's internal parameter(intrinsic) and
position and orientation in the world that is called extrinsic parameters.

<h2> (a) Intrinsic Parameters:</h2> Intrinsic parameter relate to the internal characteristics of the camera that includes:

<b>* Focal Length:</b> The focal length of the camera determines the distance between the lens and image sensor or it indicates how much the camera can zoom in and zoom out.
     
<b>* Principal Point(c_x, c_y):</b> The coordinates of the optical center which is the point where the optical axis(the imaginary line that passes from the camera's lens through its center to the image sensor) intersects the image pane.
     
<b>*Lens Distortion:</b> The camera may introduce radial distortion which can cause straight lines to appear as curved.


<h2>(b) Extrinsic Parameters:</h2> It defines the camera position and orientation in the real world, which contains:

<b>* Rotation Matrix(R):</b> It describes the camera's orientation relative to a global coordinate system. It tells you how much the camera is tilted, turned, and rolled.

<b>* Translation Vector(T):</b> It represents the camera's position in the same global coordinate system. Furthermore, it provides information on the camera's location in terms of its distance from a reference point in the world and its position along the X, Y, and Z axes.

![Screenshot from 2023-11-03 11-32-57](https://github.com/Bishow-99/Liveness-Detection/assets/80660041/abdddb46-5d29-4f08-a6ce-0b739b26c49c)


