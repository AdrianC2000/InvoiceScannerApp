import cv2


class TableExtractor:

    def __init__(self, image_path):
        self.image_path = image_path

    def extract_table(self):
        print(f"Starting extracting the table for the image: {self.image_path}")
        image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        contours = self._get_contours(image)
        return self._find_table(image, contours, 2000)

    def _get_contours(self, image):
        # Convert to gray scale image
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Simple threshold
        _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Morphological closing to improve mask
        close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        # Find only outer contours
        contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return contours

    def _find_table(self, image, contours, biggest_area):
        table = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > biggest_area:
                biggest_area = area
                x, y, width, height = cv2.boundingRect(cnt)
                table = image[y:y + height - 1, x:x + width - 1]
        return table
