import os
from tqdm import tqdm
import argparse
import cv2
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def put_dtp_label(img):
    fontScale = 4
    color = (0, 255, 255)
    org = (100, 150)
    return cv2.putText(img, 'DTP', org, cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, color, 6, cv2.LINE_AA)

def load_labels(path):
    confs = []
    for label in os.listdir(path):
        with open(os.path.join(path, label), 'r') as file:
            lines = file.readlines()
            for line in lines:
                _, x, y, w, h, conf = [float(t) for t in line.split(" ")]
                confs.append((int(label.split('.')[0]),conf))
    return confs

def logic(labelpath, confthesh=0.7, thresh=10):
    confs = load_labels(labelpath)
    proof_count = 0
    lowerbound = 10**10
    for ind,conf in confs:
        if conf>confthesh:
            lowerbound = min(ind, lowerbound)
            proof_count+=1
    if proof_count>thresh:
        return True, lowerbound
    else:
        return False, None


def video2images(filepath):
    cap = cv2.VideoCapture(filepath)
    images = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        images.append(frame)

    cap.release()
    return images

def detected_img(imgpath, lowerbound):
    detected = dict()
    for file in os.listdir(imgpath):
        if not file.endswith((".jpg")):
            continue
        num = int(file.split('.')[0])
        if num >= lowerbound:
            detected[num] = cv2.imread(os.path.join(imgpath, file))

    return detected

def proof_video(imgpath, videopath, labelpath, conf, thresh, save_path):
    dtp, lowerbound = logic(labelpath, conf, thresh)
    if not dtp:
        return False

    images = video2images(videopath)
    detected = detected_img(imgpath, lowerbound)

    for i,img in detected.items():
        images[i] = img

    images = images[lowerbound:]
    save_video(images, save_path)
    return True

def save_video(frames, save_path):
    try:
        fps, w, h = 30, frames[0].shape[1], frames[0].shape[0]
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

        for frame in frames:
            frame = put_dtp_label(frame)
            out.write(frame)
        out.release()
    except Exception as e:
        print("video can't be saved")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'videos', help='path to *.mp4 files')
    parser.add_argument('--proofpath', type=str, default=ROOT / 'proof', help='path to proof videos')
    parser.add_argument('--detectionpath', type=str, default=ROOT / 'detection_results', help='path to detection results')
    parser.add_argument('--conf', type=float, default=0.7, help='confidence for object detector')
    parser.add_argument('--thresh', type=int, default=10, help='min image for proof')
    opt = parser.parse_args()
    print(opt)
    os.makedirs(opt.proofpath, exist_ok=True)

    for file in os.listdir(opt.source):
        folder = file.split(".")[0]
        is_dtp = proof_video(imgpath = os.path.join(opt.detectionpath, folder),
                             videopath=os.path.join(opt.source, file),
                             labelpath=os.path.join(opt.detectionpath, folder, "labels"),
                             conf = opt.conf, thresh=opt.thresh,
                             save_path=os.path.join(opt.proofpath, file))
        print(file," is_dtp: ",is_dtp)

