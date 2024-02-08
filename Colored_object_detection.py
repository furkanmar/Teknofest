import cv2
import numpy as np
import time  # Eklenen kütüphane

def detect_color(image, target_color):
    # Convert the image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for detection (blue, green, yellow, and red)
    color_ranges = {
        'blue': ([100, 50, 50], [120, 255, 255]),  # Adjusted for blue
        'green': ([40, 50, 50], [80, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'red': ([0, 100, 100], [10, 255, 255]) + ([170, 100, 100], [180, 255, 255]),  # Adjusted for red (considering wrap-around)
    }

    # Get the color range for the target color
    target_range = color_ranges.get(target_color.lower())

    if target_range is None:
        return None, None  # Return None for both detected color and bounding box

    # Create a mask based on the color range in the HSV image
    mask = cv2.inRange(hsv_image, np.array(target_range[0]), np.array(target_range[1]))

    # Apply the mask and find contours
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_color = None
    bounding_box = None

    for contour in contours:
        # Filter out small contours
        if cv2.contourArea(contour) > 5000:  # Adjust this threshold based on your needs
            # Get the bounding rectangle around the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Get the region of interest (ROI)
            roi = masked_image[y:y+h, x:x+w]

            # Calculate the mean color of the ROI in the HSV space
            mean_color_hsv = cv2.mean(roi)[:3]

            # Check if the mean color is close to the color range
            if target_color.lower() == 'red' and (mean_color_hsv[0] > 170 or mean_color_hsv[0] < 10):
                detected_color = target_color
                bounding_box = (x, y, w, h)
                return detected_color, bounding_box
            elif target_color.lower() != 'red' and mean_color_hsv[0] > target_range[0][0] and mean_color_hsv[0] < target_range[1][0]:
                detected_color = target_color
                bounding_box = (x, y, w, h)
                return detected_color, bounding_box

    return detected_color, bounding_box

def draw_circle(image, center, bgr_color):
    # Draw a filled circle around the center with the specified color
    cv2.circle(image, center, 50, bgr_color, -1)

# Start the camera connection
cap = cv2.VideoCapture(0)

# Define the color sequence
color_sequence = ['red', 'blue', 'yellow', 'green']

for target_color in color_sequence:
    # Capture a frame from the camera
    ret, image = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        break

    cv2.putText(image, f"Searching for {target_color} object...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Frame', image)
    cv2.waitKey(1000)  # Wait for 1 second

    start_time = time.time()  # Başlangıç zamanını kaydet

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Detect the color and get bounding box
        detected_color, bounding_box = detect_color(frame, target_color)

        if detected_color is not None:
            # Display the detected color on the camera window with a bigger font
            cv2.putText(frame, f"{detected_color.capitalize()} object found!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Display message indicating that everything in the bounding box is of the detected color
            cv2.putText(frame, f"Everything in the bounding box is {detected_color.capitalize()}.", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            
            if bounding_box is not None:
                # Draw a circle on the center of the bounding box (example: green circle)
                draw_circle(frame, (bounding_box[0] + bounding_box[2] // 2, bounding_box[1] + bounding_box[3] // 2), (0, 255, 0))
            
            cv2.imshow('Frame', frame)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 3:  # Wait for 3 seconds
                break

        # Show the image
        cv2.imshow('Frame', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera connection and close the window
cap.release()
cv2.destroyAllWindows()
