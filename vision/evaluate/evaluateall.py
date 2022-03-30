import cv2
import xlsxwriter
from tqdm.auto import tqdm

from vision import balldetection
from vision.dataset import Color, get_dataset
from vision.evaluate.metrics import summary
from vision.evaluate.metrics.bounding_box import BoundingBox
from vision.evaluate.metrics.enumerators import BBType


def to_pred_bbox(image_name: str, color: Color, xywh: tuple[int, int, int, int]):
    return BoundingBox(image_name, color.name, xywh, bb_type=BBType.DETECTED, confidence=1.0)


algorithms = [
    # balldetection.algorithms.houghCircles,
    balldetection.algorithms.circularity,
    balldetection.algorithms.circularityConvex,
    balldetection.algorithms.circularityMoments,
    balldetection.algorithms.circularityConvexMoments,
    balldetection.algorithms.RANSAC,
    balldetection.algorithms.cannyRANSAC,
]

# Make workbook
print("Creating spreadsheet...")
workbook = xlsxwriter.Workbook('metrics.xlsx')
worksheet = workbook.add_worksheet("Metrics")

red_format = workbook.add_format()
red_format.set_bg_color("#ff0000")

blue_format = workbook.add_format()
blue_format.set_bg_color("#0000ff")
blue_format.set_font_color("#ffffff")

yellow_format = workbook.add_format()
yellow_format.set_bg_color("#ffff00")

green_format = workbook.add_format()
green_format.set_bg_color("#00ff00")

black_format = workbook.add_format()
black_format.set_bg_color("#000000")
black_format.set_font_color("#ffffff")

algorithms_format = workbook.add_format()
algorithms_format.set_bg_color("#bebebe")

headers = ["Precision[blue]@.50", "Precision[red]@.50", "AveragePrecision@.50", "Recall[blue]@.50",
           "Recall[red]@.50", "AverageRecall@.50", "F1[blue]@.50", "F1[red]@.50", "AverageF1@.50",
           "Precision[blue]@.75",
           "Precision[red]@.75", "AveragePrecision@.75", "Recall[blue]@.75", "Recall[red]@.75", "AverageRecall@.75",
           "F1[blue]@.75", "F1[red]@.75", "AverageF1@.75", "AR[red]", "AR[blue]", "mAR"]

maxWidths = []
for i, header in enumerate(["Algorithm"] + headers):
    if "red" in header:
        worksheet.write(0, i, header, red_format)
    elif "blue" in header:
        worksheet.write(0, i, header, blue_format)
    elif "Average" in header:
        worksheet.write(0, i, header, yellow_format)
    elif "Algorithm" in header:
        worksheet.write(0, i, header, black_format)
    elif "mAR" in header:
        worksheet.write(0, i, header, green_format)
    else:
        worksheet.write(0, i, header)

    width = len(header)
    maxWidths.append(width)

# Get dataset & generate ground truth
dataset = get_dataset()
cached_images = {photo.name: cv2.imread(photo.img_path) for photo in dataset}
gt = [cargo.to_groundtruth_bbox(photo.name) for photo in dataset for cargo in photo.cargos]

print("Mesuring algorithms...")
for i, alg in enumerate(algorithms):
    print(f"Mesuring {alg.__name__}...")

    # Generate predictions
    preds = [to_pred_bbox(photo.name, color, box) for photo in tqdm(dataset) for color in Color for box in
             alg(cached_images[photo.name], color)]

    # Calculate metrics
    metrics = summary.get_summary(gt, preds)

    # Write to Excel sheet
    worksheet.write(i + 1, 0, alg.__name__, algorithms_format)
    width = len(alg.__name__)
    if width > maxWidths[0]:
        maxWidths[0] = width

    for j, key in enumerate(headers):
        worksheet.write(i + 1, j + 1, metrics[key])
        width = len(str(metrics[key]))
        if width > maxWidths[j + 1]:
            maxWidths[j + 1] = width

print("Applying auto-fit...")
for i, maxWidth in enumerate(maxWidths):
    worksheet.set_column(i, i, maxWidth)

workbook.close()
