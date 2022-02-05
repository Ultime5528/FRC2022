import numpy as np

from vision.evaluate import evaluate
from vision.evaluate.metrics.bounding_box import BoundingBox
from vision.dataset import Color, get_dataset
from vision.evaluate.metrics.enumerators import BBType
from vision.evaluate.metrics.summary import get_coco_summary, get_coco_metrics


def func(img: np.ndarray, color: Color):
    return [(0, 0, 300, 300)] if color == Color.RED else [(0, 0, 300, 300)]

# evaluate(func)

def to_pred_bbox(image_name: str, color: Color, xywh: tuple[int, int, int, int]):
    return BoundingBox(image_name, color.name, xywh, bb_type=BBType.DETECTED, confidence=1.0)

dataset = get_dataset()
gt = [cargo.to_groundtruth_bbox(photo.name) for photo in dataset for cargo in photo.cargos]
preds = [to_pred_bbox(photo.name, color, box) for photo in dataset for color in Color for box in func(None, color)]

summ = get_coco_summary(gt, preds)
det = get_coco_metrics(gt, preds, iou_threshold=0.1)
# import logging
# from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
# from pathlib import Path
# import time
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     path = Path(__file__).parent.absolute()
#     event_handler = LoggingEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     print("Started")
#     try:
#         while True:
#             time.sleep(1)
#     finally:
#         observer.stop()
#         observer.join()
