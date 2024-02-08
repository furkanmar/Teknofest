import cv2
import numpy as np

def detect_color(image):
    # Convert the image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for detection (blue, green, yellow, and red)
    color_ranges = {
        'blue': ([90, 50, 50], [130, 255, 255]),
        'green': ([40, 50, 50], [80, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'red': ([0, 100, 100], [10, 255, 255]),
    }

    detected_color = None

    for color_name, (lower, upper) in color_ranges.items():
        # Create a mask based on the color range in the HSV image
        mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))

        # Apply the mask and find contours
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > 100:
                # Draw a bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Get the region of interest (ROI)
                roi = masked_image[y:y+h, x:x+w]

                # Calculate the mean color of the ROI in the HSV space
                mean_color_hsv = cv2.mean(roi)[:3]

                # Check if the mean color is close to the color range
                if mean_color_hsv[0] > 170 or mean_color_hsv[0] < 10:  # Red hue values wrap around
                    detected_color = color_name
                    return detected_color

    return detected_color

# Start the camera connection
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Detect the color
    detected_color = detect_color(frame)

    if detected_color is not None:
        # Display the detected color on the camera window with a bigger font
        cv2.putText(frame, f"Detected color: {detected_color}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the image
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera connection and close the window
cap.release()
cv2.destroyAllWindows()
