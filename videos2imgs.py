import os
import cv2
from tqdm import tqdm
import argparse
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def video2images(filepath, savepath, when=3):
    os.makedirs(savepath, exist_ok=True)
    cap = cv2.VideoCapture(filepath)
    images = []
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % when == 0:
            images.append((count,frame))
        count += 1
    for (i,img) in images:
        cv2.imwrite(os.path.join(savepath, str(i) + ".jpg"), img)

    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'videos', help='path to *.mp4 files')
    parser.add_argument('--savepath', type=str, default=ROOT / 'videos2images', help='path to save images')
    parser.add_argument('--when', type=int, default=15, help='save ever x frame')

    opt = parser.parse_args()
    os.makedirs(opt.savepath, exist_ok=True)
    for file in tqdm(os.listdir(opt.source)):
        video2images(os.path.join(opt.source, file), os.path.join(opt.savepath, file.split(".")[0]), when=opt.when)

