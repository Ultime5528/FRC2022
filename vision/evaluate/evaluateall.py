import cv2
from tqdm.auto import tqdm
import xlsxwriter

from vision.evaluate.metrics.bounding_box import BoundingBox
from vision.dataset import Color, get_dataset
from vision.evaluate.metrics.enumerators import BBType
from vision.evaluate.metrics import summary
from vision import balldetection


def to_pred_bbox(image_name: str, color: Color, xywh: tuple[int, int, int, int]):
    return BoundingBox(image_name, color.name, xywh, bb_type=BBType.DETECTED, confidence=1.0)


algorithms = [
    balldetection.algorithms.houghCircles,
    balldetection.algorithms.circularity,
    balldetection.algorithms.circularityConvex,
    balldetection.algorithms.circularityMoments,
    balldetection.algorithms.circularityConvexMoments,
    balldetection.algorithms.RANSAC,
    balldetection.algorithms.cannyRANSAC,
]

# Make workbook
workbook = xlsxwriter.Workbook('metrics.xlsx')
worksheet = workbook.add_worksheet()

headers = ["Precision[blue]@.50", "Precision[red]@.50", "AveragePrecision@.50", "Recall[blue]@.50",
 "Recall[red]@.50", "AverageRecall@.50", "F1[blue]@.50", "F1[red]@.50", "AverageF1@.50", "Precision[blue]@.75",
 "Precision[red]@.75", "AveragePrecision@.75", "Recall[blue]@.75", "Recall[red]@.75", "AverageRecall@.75",
 "F1[blue]@.75", "F1[red]@.75", "AverageF1@.75", "AR[red]", "AR[blue]", "mAR"]

for i, header in enumerate(["Algorithm"] + headers):
    worksheet.write(0, i, header)

# Get dataset & generate ground truth
dataset = get_dataset()
cached_images = {photo.name:cv2.imread(photo.img_path) for photo in dataset}
gt = [cargo.to_groundtruth_bbox(photo.name) for photo in dataset for cargo in photo.cargos]

for i, alg in enumerate(algorithms):
    # Generate predictions
    preds = [to_pred_bbox(photo.name, color, box) for photo in tqdm(dataset) for color in Color for box in alg(cached_images[photo.name], color)]

    # Calculate metrics
    metrics = summary.get_summary(gt, preds)

    # Write to Excel sheet
    worksheet.write(i+1, 0, alg.__name__)

    for j, key in enumerate(headers):
        worksheet.write(i + 1, j+1, metrics[key])

workbook.close()