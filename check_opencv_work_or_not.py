import cv2
import numpy as np

# Create a black image
popup_screen = 255 * np.ones((480, 640, 3), dtype=np.uint8)

# Display the black window
cv2.imshow('Popup Screen', popup_screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
