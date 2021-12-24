# Use finger control the cursor of computer
This software allows users to control the cursor with finger movement. The cursor follows the position of the middle finger. When fingers (thumb and index finger) are twisted together, the cursor press. When they separate, the cursor is release. Adjust parameters to fit your computer.
 
 
## Techniques used
Use OpenCV library to process images from camera.

Use a pre-trained model from the mediapipe library to identify the finger's 3D position.

Use the pynput library to control the cursor/mouse.

## Future Work 
Need to make the cursor movement smooth. In the current version, the cursor vibrates even the figure doesn't move.

Need to make cursor follows index finger rather than middle finger (I think it would make better user experience). I didn't simply make the cursor follow the index finger because when the cursor will move when twisting, this makes cursor not press down accurately. Need to think about how to predict the behavior of user so the cursor won't move when press.

Need to consider 3D space distance between thumb and index finger when making judgment of twist action. The current code only considers two dimensions (x and y) because I don't know how to convert the z value into real-world distance (the row data is a decimal number). Need to fix this issue or the cursor will press when two fingers do not twist but overlapped in 2D dimension (in camera's view)

# Demo
Video: [![Watch the video]](https://www.youtube.com/watch?v=UueDitx1ZLE)
