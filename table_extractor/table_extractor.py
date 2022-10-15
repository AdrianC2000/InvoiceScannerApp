import cv2


class TableExtractor:

    def __init__(self, image):
        self.image = image

    def extract_table(self):
        contours = self._get_contours()
        return self._find_table(contours, 2000)

    def _get_contours(self):
        # Convert to gray scale image
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        # Simple threshold
        _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Morphological closing to improve mask
        close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        # Find only outer contours
        contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return contours

    def _find_table(self, contours, biggest_area):
        table = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > biggest_area:
                biggest_area = area
                x, y, width, height = cv2.boundingRect(cnt)
                try:
                    table = self.image[y - 2:y + height + 2, x - 2:x + width + 2]
                except IndexError:
                    table = self.image[y:y + height, x:x + width]
        return table