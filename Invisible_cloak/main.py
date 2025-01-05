import cv2  # OpenCV library for computer vision tasks
import numpy as np  # NumPy for numerical operations

# Function to create a mask for detecting a specific color in the frame
def create_mask(frame, lower_color, upper_color):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a binary mask where the specified color range is white, and everything else is black
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply morphological opening to remove small noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # Apply morphological dilation to expand the detected regions
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    return mask

# Function to apply the invisibility effect using the mask and background
def apply_cloak_effect(frame, mask, background):
    # Invert the mask to get areas that are not part of the detected color
    mask_inv = cv2.bitwise_not(mask)
    # Extract the foreground (everything except the detected color)
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    # Extract the background where the detected color is
    bg = cv2.bitwise_and(background, background, mask=mask)
    # Combine the foreground and background to create the final effect
    return cv2.add(fg, bg)

def main():
    print("OpenCV version:", cv2.__version__)  # Print the OpenCV version being used
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Warming up the camera...")
    for _ in range(60):  # Allow the camera to adjust to lighting conditions
        _, _ = cap.read()

    print("Capturing background image...")
    _, background = cap.read()  # Capture a frame to use as the background
    background = cv2.flip(background, 1)  # Flip the background image horizontally

    # Define HSV color ranges for detecting red color
    lower_red1 = np.array([0, 150, 100])  # Lower range of red (hue 0-10)
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 100])  # Upper range of red (hue 170-180)
    upper_red2 = np.array([180, 255, 255])

    print("Starting invisibility effect...")
    while True:
        ret, frame = cap.read()  # Capture a frame from the camera
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror effect
        # Create masks for the two red color ranges
        mask1 = create_mask(frame, lower_red1, upper_red1)
        mask2 = create_mask(frame, lower_red2, upper_red2)
        # Combine the masks to detect all shades of red
        mask = cv2.bitwise_or(mask1, mask2)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Create a new mask to filter out small contours
        mask_filtered = np.zeros_like(mask)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Ignore small areas
                cv2.drawContours(mask_filtered, [contour], -1, 255, thickness=cv2.FILLED)

        # Apply the invisibility effect using the filtered mask
        result = apply_cloak_effect(frame, mask_filtered, background)

        cv2.imshow("Invisibility Cloak", result)  # Display the result in a window
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
