import itertools
from multiprocessing import Pool

import cv2
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from vision import balldetection
from vision.dataset import Color, get_dataset
from vision.evaluate.metrics import summary
from vision.evaluate.metrics.bounding_box import BoundingBox
from vision.evaluate.metrics.enumerators import BBType


def to_pred_bbox(image_name: str, color: Color, xywh: tuple[int, int, int, int]):
    return BoundingBox(image_name, color.name, xywh, bb_type=BBType.DETECTED, confidence=1.0)


dataset = get_dataset()
cached_images = {photo.name: cv2.imread(photo.img_path) for photo in dataset}
gt = [cargo.to_groundtruth_bbox(photo.name) for photo in dataset for cargo in photo.cargos]


# def iterate(value):
#     # for rs, rv, bs, bv, minr in tqdm(list(itertools.product(range(90, 150, 10), range(30, 120, 10), range(90, 150, 10), range(30, 120, 10),np.arange(0.01, 0.05, 0.005)))):
#     rs, rv, bs, bv, minr = value
#     preds = [to_pred_bbox(photo.name, color, box) for photo in dataset for color in Color for box in balldetection.algorithms.circularityMoments(cached_images[photo.name], color, minRadiusPerc=minr, rs=rs, rv=rv, bs=bs, bv=bv)]
#
#     metrics = summary.get_summary(gt, preds)
#     metrics["rs"] = rs
#     metrics["rv"] = rv
#     metrics["bs"] = bs
#     metrics["bv"] = bv
#     metrics["minr"] = minr
#
#     metrics = {k: metrics[k] for k in ["rs", "rv", "bs", "bv", "minr", "Precision[blue]@.50", "Precision[red]@.50", "AveragePrecision@.50", "Recall[blue]@.50",
#                                "Recall[red]@.50", "AverageRecall@.50", "F1[blue]@.50", "F1[red]@.50", "AverageF1@.50",
#                                "Precision[blue]@.75",
#                                "Precision[red]@.75", "AveragePrecision@.75", "Recall[blue]@.75", "Recall[red]@.75",
#                                "AverageRecall@.75",
#                                "F1[blue]@.75", "F1[red]@.75", "AverageF1@.75", "AR[red]", "AR[blue]", "mAR"]}
#
#     return metrics

def iterate(value):
    maxi, d, inl = value
    preds = [to_pred_bbox(photo.name, color, box) for photo in dataset for color in Color for box in
             balldetection.algorithms.RANSAC(cached_images[photo.name], color, maxIterations=maxi,
                                             threshold_distance_percentage=d, threshold_inlier_count=inl)]

    metrics = summary.get_summary(gt, preds)
    metrics["maxi"] = maxi
    metrics["d"] = d
    metrics["inl"] = inl

    metrics = {k: metrics[k] for k in
               ["maxi", "d", "inl", "Precision[blue]@.50", "Precision[red]@.50", "AveragePrecision@.50",
                "Recall[blue]@.50",
                "Recall[red]@.50", "AverageRecall@.50", "F1[blue]@.50", "F1[red]@.50", "AverageF1@.50",
                "Precision[blue]@.75",
                "Precision[red]@.75", "AveragePrecision@.75", "Recall[blue]@.75", "Recall[red]@.75",
                "AverageRecall@.75",
                "F1[blue]@.75", "F1[red]@.75", "AverageF1@.75", "AR[red]", "AR[blue]", "mAR"]}

    return metrics


if __name__ == "__main__":
    # values = list(itertools.product(range(90, 140, 10), range(40, 100, 10), range(90, 140, 10), range(40, 100, 10),np.arange(0.01, 0.05, 0.01)))
    values = list(itertools.product(range(10, 60, 10), np.arange(0.05, 0.3, 0.01), range(40, 150, 10)))

    with Pool(3) as p:
        summs = list(tqdm(p.imap(iterate, values), total=len(values)))

    df = pd.DataFrame(summs)

    df.to_excel("params.xlsx")
