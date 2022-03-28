import base64
import inspect
from pathlib import Path
from typing import List, Tuple, Callable, Dict

import cv2
import eel
import numpy as np
import watchdog.events
from tqdm.auto import tqdm
from watchdog.observers import Observer

from ..dataset import get_dataset, Color, Photo, Cargo

VisionAlgorithm = Callable[[np.ndarray, Color], List[Tuple[int, int, int, int]]]


class ModifiedEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, func):
        self.func = func

    def on_modified(self, event):
        self.func()


def image_to_base64(img):
    _, jpeg = cv2.imencode('.jpg', img)
    bytes_data = jpeg.tobytes()
    blob = base64.b64encode(bytes_data)
    blob = blob.decode("utf-8")
    return "data:image/jpeg;base64," + blob


def annotate_photo(
        img: np.ndarray,
        targets: List[Cargo],
        preds: Dict[Color, List[Tuple[int, int, int, int]]],
):
    for cargo in targets:
        cv2.rectangle(img, (cargo.left, cargo.top), (cargo.right, cargo.bottom), (0, 255, 0), thickness=1)

    for color, rects in preds.items():
        for x, y, w, h in rects:
            cv2.rectangle(img, (x, y), (x + w, y + h), color.bgr, thickness=2)

    return img


class EelEvaluate:
    max_size = 1000
    alpha = 0.25

    def __init__(self, func: VisionAlgorithm):
        self.func = func
        self.cache_dataset()
        eel.expose(self.eval)

    def cache_dataset(self):
        print("Caching dataset in memory...")
        self.dataset: List[Photo] = get_dataset()
        self.images: Dict[str, np.ndarray] = dict()

        for photo in tqdm(self.dataset):
            img = cv2.imread(photo.img_path)

            h, w, _ = img.shape
            f = self.max_size / h if h > w else self.max_size / w
            if f < 1:
                img = cv2.resize(img, None, fx=f, fy=f)
                photo.resize_cargos(f)

            self.images[photo.name] = img
        print("Cached dataset in memory.")

    def start(self):
        web_folder = Path(__file__).parent / ".client"
        eel.init(web_folder, allowed_extensions=['.js'])
        self._start_file_observer()
        eel.start("index.html", mode='edge')
        self._stop_file_observer()

    def _start_file_observer(self):
        self.observer = Observer()
        dir_path = Path(inspect.getfile(self.func)).parent.absolute()
        self.observer.schedule(watchdog.events.LoggingEventHandler(), dir_path, recursive=True)
        self.observer.start()
        print(f"Observing dir '{dir_path}'")

    def _stop_file_observer(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def eval(self):
        eel.spawn(self._eval)

    def _eval(self):
        filenames = list(map(lambda p: p.name, self.dataset))
        eel.setPhotoNames(filenames)()
        print("Sent photo names")

        for photo in self.dataset:
            cached_img = self.images[photo.name].copy()
            preds = {color: self.func(cached_img, color) for color in Color}
            cached_img = annotate_photo(cached_img, photo.cargos, preds)

            eel.setPhotoData({
                "name": photo.name,
                "data": image_to_base64(cached_img)
            })()
            eel.sleep(0.001)


def evaluate(func: VisionAlgorithm):
    import logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    inst = EelEvaluate(func)
    inst.start()


if __name__ == '__main__':
    from ..balldetection import algorithms

    evaluate(algorithms.RANSAC)
