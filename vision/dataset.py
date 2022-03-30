import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List

import supervisely_lib as sly
from dotenv import load_dotenv
from supervisely_lib.annotation.label import Label
from tqdm.auto import tqdm

from .color import Color
from .evaluate.metrics.bounding_box import BoundingBox, BBFormat

TEAM_NAME = "Ultime 5528"
WORKSPACE_NAME = "FRC 2022"
PROJECT_NAME = "cargo_resized"
DATASET_DIR = Path(__file__).parent / "dataset_cache"


@dataclass
class Cargo:
    color: Color
    left: int
    top: int
    right: int
    bottom: int

    @classmethod
    def from_supervisely_label(cls, label: Label):
        geo = label.geometry
        return cls(Color(label.obj_class.name), geo.left, geo.top, geo.right, geo.bottom)

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def resize(self, f: float):
        self.left = math.floor(self.left * f)
        self.top = math.floor(self.top * f)
        self.right = math.ceil(self.right * f)
        self.bottom = math.ceil(self.bottom * f)

    def to_groundtruth_bbox(self, image_name: str) -> BoundingBox:
        return BoundingBox(
            image_name,
            self.color.name,
            (self.left, self.top, self.right, self.bottom),
            format=BBFormat.XYX2Y2)


class Photo:
    def __init__(self, img_path: str, cargos: List[Cargo]):
        self.img_path = img_path
        self.name = Path(self.img_path).name
        self.cargos = cargos

    def resize_cargos(self, f):
        for cargo in self.cargos:
            cargo.resize(f)


def download_dataset():
    # https://supervise.ly/explore/notebooks/download-project-26/overview

    if DATASET_DIR.exists():
        raise FileExistsError(f"Le dossier {DATASET_DIR} existe déjà. Pour l'écraser, utilisez la commande 'update'.")

    load_dotenv()
    try:
        # Open existing project on disk.
        api = sly.Api.from_env()
    except KeyError:
        raise FileNotFoundError("Votre fichier .env ne contient pas les valeurs nécessaires")

    team = api.team.get_info_by_name(TEAM_NAME)
    if team is None:
        raise RuntimeError("Team {!r} not found".format(TEAM_NAME))

    workspace = api.workspace.get_info_by_name(team.id, WORKSPACE_NAME)
    if workspace is None:
        raise RuntimeError("Workspace {!r} not found".format(WORKSPACE_NAME))

    project = api.project.get_info_by_name(workspace.id, PROJECT_NAME)
    if project is None:
        raise RuntimeError("Project {!r} not found".format(PROJECT_NAME))

    print(f"Team: id={team.id}, name={team.name}")
    print(f"Workspace: id={workspace.id}, name={workspace.name}")
    print(f"Project: id={project.id}, name={project.name}")

    # create Project object for writing data in supervisely format
    project_fs = sly.Project(str(DATASET_DIR), sly.OpenMode.CREATE)

    # download meta of remote project and save it to directory
    meta_json = api.project.get_meta(project.id)
    meta = sly.ProjectMeta.from_json(meta_json)
    project_fs.set_meta(meta)

    # iterate over remote datasets and images, download image and corresponding annotation,
    # save item (img+ann pair) to directory
    for dataset in api.dataset.get_list(project.id):
        dataset_fs = project_fs.create_dataset(dataset.name)

        images = api.image.get_list(dataset.id)
        with tqdm(total=len(images), desc="Process") as progress_bar:
            for batch in sly.batched(images, batch_size=10):
                image_ids = [image_info.id for image_info in batch]
                image_names = [image_info.name for image_info in batch]

                # download images in numpy format
                img_nps = api.image.download_nps(dataset.id, image_ids)

                # download annotations in json format
                ann_infos = api.annotation.download_batch(dataset.id, image_ids)
                ann_jsons = [ann_info.annotation for ann_info in ann_infos]

                for name, img, ann in zip(image_names, img_nps, ann_jsons):
                    dataset_fs.add_item_np(name, img, ann)

                progress_bar.update(len(batch))

    print(f"Project {PROJECT_NAME} has been successfully downloaded in {DATASET_DIR}")
    print("Total number of images: ", project_fs.total_items)


def get_dataset() -> List[Photo]:
    if not (DATASET_DIR / "meta.json").exists():
        print(f"Le dossier {DATASET_DIR} ne contient pas les images.")
        print("Téléchargement des images...")
        download_dataset()

    project_fs = sly.Project(str(DATASET_DIR), sly.OpenMode.READ)

    all_items = []

    for dataset in list(project_fs.datasets):
        for item_name in dataset:
            paths = dataset.get_item_paths(item_name)
            ann = sly.Annotation.load_json_file(paths.ann_path, project_fs.meta)
            cargos = list(map(Cargo.from_supervisely_label, ann.labels))
            all_items.append(Photo(paths.img_path, cargos))

    return all_items


def update_dataset():
    if DATASET_DIR.exists():
        print(f"Suppression de {DATASET_DIR}...")
        shutil.rmtree(DATASET_DIR)
    download_dataset()


if __name__ == '__main__':
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser()
    sub = parser.add_subparsers()

    sub_download = sub.add_parser("download", help="Download the dataset from Supervise.ly")
    sub_download.set_defaults(func=download_dataset)

    sub_update = sub.add_parser("update", help="Update the dataset from Supervise.ly")
    sub_update.set_defaults(func=update_dataset)

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    options = parser.parse_args()
    options.func()
