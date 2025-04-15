import cv2

image = cv2.imread("C:/Users/saksh/Documents/Guesture Application/sakshi photo passport.jpeg")  # Replace with your image path
zoom_factor = 1.0

while True:
    h, w, _ = image.shape
    new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
    x1, y1 = (w - new_w) // 2, (h - new_h) // 2

    zoomed_image = image[y1:y1 + new_h, x1:x1 + new_w]
    zoomed_image = cv2.resize(zoomed_image, (w, h))

    cv2.putText(zoomed_image, f"Zoom: {zoom_factor:.2f}x", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Image Zoom", zoomed_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('+'):  # Zoom In
        zoom_factor = min(2.0, zoom_factor + 0.1)
    elif key == ord('-'):  # Zoom Out
        zoom_factor = max(1.0, zoom_factor - 0.1)
    elif key == ord('q'):  # Quit
        break

cv2.destroyAllWindows()
