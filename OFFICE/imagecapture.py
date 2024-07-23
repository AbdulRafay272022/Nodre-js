import cv2
import os
import time

# Directory to save captured frames
output_dir = r'C:\Users\Lenovo\Downloads\allfiles2\capture'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the default camera (usually the built-in webcam)
video_capture = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not video_capture.isOpened():
    print("Error: Unable to open camera")
    exit()

# Start frame index
frame_index = 0
start_time=time.time()
# Read frames from the camera and save them as images
while True:
    # Read a frame from the camera
    ret, frame = video_capture.read()
    
    # If frame reading was successful
    if ret:
        # Save the frame as an image
        output_file = os.path.join(output_dir, f"frame_{frame_index:04d}.jpg")
        cv2.imwrite(output_file, frame)
        
        # Increment frame index
        frame_index += 1
        
        # Display the captured frame
        cv2.imshow('Captured Frame', frame)
        
        # Press 'q' to quit capturing frames
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error: Unable to capture frame")
        break
end_time=time.time()
# Release the video capture object
video_capture.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

print(f"{frame_index} frames captured and saved in {output_dir}")
print(end_time-start_time)
