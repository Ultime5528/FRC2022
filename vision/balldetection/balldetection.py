import cv2
import numpy as np
import math
from enum import Enum
from skimage.morphology import skeletonize
from scipy.optimize import minimize
from typing import List, Optional
from dataclasses import dataclass
from ..dataset import Color


def maskColor(img: np.ndarray, color: Color, rs: Optional[int]=None, rv: Optional[int]=None, bs: Optional[int]=None, bv: Optional[int]=None) -> np.ndarray:
    """
    :param img: Source image, BGR
    :param color: Color to mask
    :return: A binary mask of only the color to keep
    """
    # blurred = cv2.medianBlur(img, 15)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == Color.RED:
        mask1 = cv2.inRange(hsv, (0, rs or 120, rv or 70), (7, 255, 255)) #cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (163, rs or 120, rv or 70), (180, 255, 255)) #cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)
    elif color == Color.BLUE:
        mask = cv2.inRange(hsv, (87, bs or 100, bv or 60), (112, 255, 255)) #cv2.inRange(hsv, (90, 86, 50), (130, 255, 255))
    else:
        raise Exception("No valid color was passed!")

    return mask


def findColorContours(img: np.ndarray, color, rs: Optional[int]=None, rv: Optional[int]=None, bs: Optional[int]=None, bv: Optional[int]=None) -> np.ndarray:
    """
    :param img: Source image, BGR
    :param color: Color of the contours to find
    :return: The detected contours of the corresponding color
    """
    mask = maskColor(img, color, rs, rv, bs, bv)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return cnts


def filterCircles(contours: np.ndarray, error: float) -> np.ndarray:
    """
    :param contours: Contours to filter
    :param error: Allowable error of circularity
    :return: A list of contours from the original set that most likely are circles
    """
    circles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        circularity = 4 * math.pi * area / (perimeter * perimeter) if perimeter else 0

        if abs(1 - circularity) <= error:
            circles.append(cnt)

    return circles


def filterCirclesMoments(contours: np.ndarray, error: float) -> np.ndarray:
    """
    :param contours: Contours to filter
    :param error: Allowable error of circularity
    :return: A list of contours from the original set that most likely are circles, using Moments
    """
    circles = []
    for cnt in contours:
        M = cv2.moments(cnt)
        circularity = (M["m00"] * M["m00"]) / (2 * math.pi * (M["mu20"] + M["mu02"])) if M["m00"] else 0

        if abs(1 - circularity) <= error:
            circles.append(cnt)

    return circles


def convexContours(contours: np.ndarray) -> np.ndarray:
    """
    :param contours: Contours to wrap into a convex hull
    :return: The corresponding convex hull for every contour
    """
    return [cv2.convexHull(cnt) for cnt in contours]


def defineCircle(p1, p2, p3):
    # https://stackoverflow.com/questions/28910718/give-3-points-and-a-plot-circle
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return None, None, None

    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)

    return cx, cy, radius


@dataclass
class CandidateCircle:
    center: np.ndarray
    radius: float
    inlier_count: int
    mae: float

    def to_xywh(self):
        rect = np.array([self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2])
        return tuple(rect.round().astype(int))


def findCirclesInContours(contours: List[np.ndarray], max_iterations: int=10, threshold_distance_percentage:Optional[float] = None, threshold_inlier_count:Optional[int] = None) -> list[tuple[int, int, int, int]]:
    """
    :rtype: object
    :param contours: Contours with probable circles
    :param max_iterations: Amount of iterations to run it for
    :return: The circles found in the contours in format (x, y, w, h) (bounding rect)
    """
    threshold_distance_percentage = threshold_distance_percentage or 0.21
    threshold_inlier_count = threshold_inlier_count or 60
    rects = []

    for cnt in contours:
        # cnt.shape : (n, 1, 2)
        if cnt.shape[0] >= 3 + threshold_inlier_count:
            cnt = cnt[:, 0, :]  # shape: (n, 2)
            candidate_circles = []
            for _ in range(max_iterations):
                # Select any 3 points
                idx = np.random.choice(cnt.shape[0], 3, replace=False)
                p1 = cnt[idx[0]]
                p2 = cnt[idx[1]]
                p3 = cnt[idx[2]]

                # Find the circle passing through these 3 points. This is our candidate circle
                cx, cy, radius = defineCircle(p1, p2, p3)
                c = np.array([cx, cy])

                if not radius:
                    continue

                outer_radius = radius * (1 + threshold_distance_percentage)
                inner_radius = radius * (1 - threshold_distance_percentage)

                # Use threshold distance and find all points which lie in the doughnut region. These are the inlier
                # points.
                dist = ((cnt - c) ** 2).sum(axis=1)
                inliers = cnt[(dist < outer_radius * outer_radius) & (dist >= inner_radius * inner_radius)]

                # If the count is less than threshold inlier count then skip this candidate circle and go back to the
                # first step.
                if len(inliers) < threshold_inlier_count:
                    continue

                # Use all inliner points and determine new candidate circle
                res = minimize(lambda c: ((inliers - c) ** 2).sum(), inliers.mean(0))
                c = res.x

                r = np.mean(np.sqrt(((inliers - c) ** 2).sum(axis=1)))

                # Find all new inliner points and new  outlier points for new candidate circle
                outer_radius = radius * (1 + threshold_distance_percentage)
                inner_radius = radius * (1 - threshold_distance_percentage)

                # Use threshold distance and find all points which lie in the doughnut region. These are the inlier
                # points.
                dist = ((cnt - c) ** 2).sum(axis=1)
                inliers = cnt[(dist < outer_radius * outer_radius) & (dist >= inner_radius * inner_radius)]

                # If the count inlier points is less than threshold inlier count then skip this new candidate
                #  circle and go back to the first step.
                if len(inliers) < threshold_inlier_count:
                    continue

                # If the count exceeds threshold inlier count then move on to next step
                # Calculate the mean absolute error for the new candidate circle using the new inlier points
                mae = np.mean(np.abs(np.sqrt(((inliers - c) ** 2).sum(axis=1)) - r))

                # Add this candidate circle to the shortlist along with count of inlier points and the mean absolute
                # error
                candidate_circles.append(CandidateCircle(c, r, len(inliers), mae))

                # Go back to the first step and repeat for max iterations number of times

            # Then max iterations is completed, examine the shortlist of candidate rects and pick the circle with
            # maximum inlier count. If more than candidate rects with same inliner count then pick the candidate
            # circle with lesser mean absolute error
            if len(candidate_circles) > 0:
                best = candidate_circles[0]
                for c in candidate_circles[1:]:
                    if c.inlier_count > best.inlier_count:
                        best = c
                    elif c.inlier_count == best.inlier_count:
                        if c.mae < best.mae:
                            best = c

                rects.append(best.to_xywh())

    return rects


def findEdges(img: np.ndarray) -> np.ndarray:
    """
    :param img: Source image, BGR
    :return: A black and white image of every edge in the source image
    """
    blurred = cv2.medianBlur(img, 11)
    edges = cv2.Canny(blurred, 30, 100)
    return cv2.dilate(edges, None, anchor=(-1, -1), iterations=1)


def skeletonization(img: np.ndarray) -> np.ndarray:
    """
    :param img: Binary image to skeletonize
    :return: The skeleton of the binary image
    """
    return skeletonize(img / 255, method="lee")
