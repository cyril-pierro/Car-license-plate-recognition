import base64
from functools import singledispatchmethod
from typing import Union

import cv2
import easyocr
import imutils
import numpy as np
from fastapi import HTTPException
from pydantic import BaseSettings


class TrackerModel:
    def __init__(self) -> None:
        self._location = None
        self._reader = None

    def initialize_model(self) -> None:
        self._reader = easyocr.Reader(["en"])

    @singledispatchmethod
    def _process_input(self, image: Union[str, bytes]):
        return image

    @_process_input.register(str)
    def _(self, image: str):
        image_new = image.split(",")[-1]
        return base64.b64decode(image_new)

    def _apply_filter_and_edge_detection(self, gray_image):
        bfilter = cv2.bilateralFilter(gray_image, 11, 17, 17)
        edged_image = cv2.Canny(bfilter, 30, 200)
        return edged_image

    def _apply_contours_and_mask(self, edged_image):
        keypoints = cv2.findContours(
            edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                self._location = approx
                break
        return self._location

    def _get_area_of_text(self, original_image, gray_image, location):
        mask = np.zeros(gray_image.shape, np.uint8)
        _ = cv2.drawContours(mask, [location], 0, 255, -1)
        _ = cv2.bitwise_and(original_image, original_image, mask=mask)
        return mask

    def _extract_cropped_image(self, mask, gray_image):
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray_image[x1: x2 + 1, y1: y2 + 1]
        return cropped_image

    def _get_text_from_image(self, cropped_image):
        result = self._reader.readtext(cropped_image)
        return result

    def _perform_preprocessing(self, image: bytes):
        processed_image = self._process_input(image)
        image_as_np = np.frombuffer(processed_image, dtype=np.int8)
        new_image = cv2.imdecode(image_as_np, flags=1)
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        edged = self._apply_filter_and_edge_detection(gray)
        location = self._apply_contours_and_mask(edged)
        mask = self._get_area_of_text(new_image, gray, location)
        cropped_image = self._extract_cropped_image(mask, gray)
        return cropped_image

    def predict(self, image: Union[str, bytes]) -> str:
        try:
            new_image = self._process_input(image)
            processed_image = self._perform_preprocessing(new_image)
            results = self._get_text_from_image(processed_image)
            plate_number = [value[-2] for value in results]
            return " ".join(plate_number)
        except Exception:
            raise HTTPException(400, detail="invalid image format or parameter")


class Settings(BaseSettings):
    version: str = "1.0"
    releaseId: str = "1.1"
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "Car Tracker"


settings = Settings()
tracker = TrackerModel()
