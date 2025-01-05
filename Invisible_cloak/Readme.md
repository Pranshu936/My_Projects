# Invisibility Cloak Using Python and OpenCV

This project demonstrates a fun and interactive way to mimic Harry Potter's invisibility cloak using Python and OpenCV. By detecting a specific color range and replacing it with a background image, the program creates a real-time illusion of invisibility.

## Features
- Captures background image dynamically.
- Detects a specific color in the frame (e.g., red).
- Replaces the detected color with the background image in real-time.
- Works seamlessly with any solid color that does not overlap skin tones or the background.

## How It Works
1. The webcam captures a frame to use as the background.
2. The program detects a predefined color (red in this case) in the video feed.
3. A mask is created for the detected color.
4. The masked areas are replaced with the previously captured background image.
5. The final result is displayed in real-time, creating the invisibility effect.

## Requirements
- Python 3.x
- OpenCV
- NumPy

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Install the required libraries:
   ```bash
   pip install opencv-python numpy
   ```

## Usage
1. Run the Python script:
   ```bash
   python invisibility_cloak.py
   ```
2. Ensure your webcam is connected and functioning.
3. Place a red cloak (or any object with a predefined color) in front of the camera.
4. Watch the magic happen!

## Customization
To change the color of the cloak:
1. Modify the HSV ranges in the script:
   ```python
   lower_red1 = np.array([0, 120, 70])
   upper_red1 = np.array([10, 255, 255])
   lower_red2 = np.array([170, 120, 70])
   upper_red2 = np.array([180, 255, 255])
   ```
   Replace these values with the HSV range of your desired color.

2. Run the script again to see the effect with the new color.

## Notes
- For best results, ensure the background is static and well-lit.
- Avoid using colors that overlap with skin tones or background elements to minimize interference.

Happy coding, and enjoy creating magic! ✨

