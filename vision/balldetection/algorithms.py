import balldetection

import cv2
import numpy as np
import math

from dataclasses import dataclass


@dataclass
class Circle:
    center: np.ndarray
    radius: float

minRadiusPercDefault = 0.1 #10

def _convertToCircles(contours: np.ndarray) -> np.ndarray:
    """
    :param contours: Contours to find dimensions
    :return: The particles' corresponding center and radius in format (center x, center y, average radius)
    """
    circles = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        circles.append(Circle((x + (w // 2), y + (h // 2)), (w + h) // 4))
    return circles

def _computeMinRadius(img: np.ndarray, minRadiusPerc: float) -> int:
    """
    :param img: The image containing the radius
    :param minRadiusPerc: The minimal percentage of the image allowed for the radius
    :return: The minimal length (px) in the image allowed for the radius
    """
    return int(img.shape[0] * minRadiusPerc if img.shape[0] < img.shape[1] else img.shape[1] * minRadiusPerc)

def houghCircles(img: np.ndarray, color: balldetection.Color, error: float = 10, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param error: Distance error threshold
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 100, param1=100, param2=90, minRadius=minRadius)

    res = []
    if circles is not None:
        cnts = balldetection.findColorContours(img, color)

        circlesData = _convertToCircles(cnts)
        circlesData = filter(lambda c: c.radius > minRadius, circlesData)

        centers = [c.center for c in circlesData]

        # Arrondir les valeurs de Hough Circles en int
        circles = np.uint16(np.around(circles))

        for circle in circles[0, :]:
            for cx, cy in centers:
                if circle[0] - circle[2] + error <= cx <= circle[0] + circle[2] - error and circle[1] - circle[2] + error <= cy <= circle[1] + circle[2] - error:
                    ballX = circle[0] - circle[2]
                    ballY = circle[1] - circle[2]
                    ballWH = circle[2] * 2
                    res.append((ballX, ballY, ballWH, ballWH))

                    break

    return res


def circularity(img: np.ndarray, color: balldetection.Color, error: float = 0.5, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param error: Circularity error threshold
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    cnts = balldetection.findColorContours(img, color)
    circles = balldetection.filterCircles(cnts, error)

    res = []
    if circles is not None:
        for circle in circles:
            rect = cv2.boundingRect(circle)

            if rect[2] > minRadius*2:
                res.append(rect)
    return res

def circularityConvex(img: np.ndarray, color: balldetection.Color, error: float = 0.1, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param error: Circularity error threshold
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    cnts = balldetection.findColorContours(img, color)
    hulls = balldetection.convexContours(cnts)
    circles = balldetection.filterCircles(hulls, error)

    res = []
    if circles is not None:
        for circle in circles:
            rect = cv2.boundingRect(circle)

            if rect[2] > minRadius*2:
                res.append(rect)
    return res

def circularityMoments(img: np.ndarray, color: balldetection.Color, error: float = 0.2, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param error: Circularity error threshold
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    cnts = balldetection.findColorContours(img, color)
    circles = balldetection.filterCirclesMoments(cnts, error)

    res = []
    if circles is not None:
        for circle in circles:
            rect = cv2.boundingRect(circle)

            if rect[2] > minRadius*2:
                res.append(rect)
    return res

def circularityConvexMoments(img: np.ndarray, color: balldetection.Color, error: float = 0.05, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param error: Circularity error threshold
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    cnts = balldetection.findColorContours(img, color)
    hulls = balldetection.convexContours(cnts)
    circles = balldetection.filterCirclesMoments(hulls, error)

    res = []
    if circles is not None:
        for circle in circles:
            rect = cv2.boundingRect(circle)

            if rect[2] > minRadius*2:
                res.append(rect)
    return res

def RANSAC(img: np.ndarray, color: balldetection.Color, maxIterations: float = 10, minRadiusPerc: float = minRadiusPercDefault):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param maxIterations: Maximum RANSAC iterations
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)

    cnts = balldetection.findColorContours(img, color)
    cnts = filter(lambda x: cv2.boundingRect(x)[3] > minRadius*2, cnts)
    res = balldetection.findCirclesInContours(cnts, maxIterations)

    return res

def cannyRANSAC(img: np.ndarray, color: balldetection.Color, maxIterations: float = 30, minRadiusPerc: float = minRadiusPercDefault, ratioThreshold: float = 0.3, minColorRatio: float = 0.5):
    """
    :param img: Source image, BGR
    :param color: Color of the balls to track
    :param maxIterations: Maximum RANSAC iterations
    :param minRadiusPerc: Minimum percentage of the smallest side of the image allowed for the circles' radius
    :param minColorRatio: Minimum color in circle
    :return: The circles found in the contours in format (center x, center y, average radius)
    """
    minRadius = _computeMinRadius(img, minRadiusPerc)
    absLogRatioThreshold = abs(math.log10(ratioThreshold))

    edges = balldetection.findEdges(img)
    cnts, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    w_contours = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


    # filtrer canny
    filtered = []

    mask = balldetection.maskColor(img, color)
    cv2.imshow("mask", mask)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)

        # ratio ne s'approche pas de 1
        if abs(math.log10(w/h)) > absLogRatioThreshold:
            continue

        # trop petites (width)
        if w <= minRadius*2:
            continue

        # trop petites (height)
        if h <= minRadius*2:
            continue

        # couleur
        hull = cv2.convexHull(cnt)
        contourArea = cv2.contourArea(hull)

        mask2 = np.zeros(mask.shape, np.uint8)
        cv2.drawContours(mask2, [hull], -1, 255, -1)
        maskInContour = mask & mask2
        maskArea = cv2.countNonZero(maskInContour)

        if maskArea/contourArea <= minColorRatio:
            continue

        filtered.append(cnt)

    cv2.drawContours(w_contours, filtered, -1, (255, 0, 0), 2)
    cv2.imshow("contours", w_contours)

    res = balldetection.findCirclesInContours(filtered, maxIterations)

    return res
