import os
from tqdm import tqdm
import argparse
import cv2
from pathlib import Path
import sys
import json


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
                confs.append((int(label.split('.')[0]), conf))
    return confs


def logic(labelpath, confthesh=0.7, thresh=10):
    confs = load_labels(labelpath)
    proof_count = 0
    lowerbound = 10 ** 10
    for ind, conf in confs:
        if conf > confthesh:
            lowerbound = min(ind, lowerbound)
            proof_count += 1
    if proof_count > thresh:
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
        return False, False

    images = video2images(videopath)
    detected = detected_img(imgpath, lowerbound)

    for i, img in detected.items():
        images[i] = img

    images = images[lowerbound:]
    save_video(images, save_path)
    return True, lowerbound


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
    parser.add_argument('--detectioh_sp', type=str, default=ROOT / 'detection_sp',
                        help='path to detection results special transport')
    parser.add_argument('--detectioh_ocl', type=str, default=ROOT / 'detection_ocl',
                        help='path to detection results special transport')
    parser.add_argument('--conf_sp', type=float, default=0.7, help='confidence for object detector special transport')
    parser.add_argument('--conf_col', type=float, default=0.20, help='confidence for object detector collision')
    parser.add_argument('--thresh_sp', type=int, default=10, help='min image for proof special transport')
    parser.add_argument('--thresh_col', type=int, default=4, help='min image for proof detector collision')
    opt = parser.parse_args()
    print(opt)
    os.makedirs(opt.proofpath, exist_ok=True)
    result = {}
    ### simple logic with sp transport
    for file in os.listdir(opt.source):
        folder = file.split(".")[0]
        is_dtp, lower = proof_video(imgpath=os.path.join(opt.detectioh_sp, folder),
                                    videopath=os.path.join(opt.source, file),
                                    labelpath=os.path.join(opt.detectioh_sp, folder, "labels"),
                                    conf=opt.conf_sp, thresh=opt.thresh_sp,
                                    save_path=os.path.join(opt.proofpath, file))
        if is_dtp:
            result[file] = {"time":lower/30, "is_dtp":is_dtp}
        else:
            result[file] = {"is_dtp":is_dtp}
    print("SIMPLE IS DONE")
    ### hard logic with collision
    for file in os.listdir(opt.source):
        folder = file.split(".")[0]
        is_dtp, lower = proof_video(imgpath=os.path.join(opt.detectioh_ocl, folder),
                                    videopath=os.path.join(opt.source, file),
                                    labelpath=os.path.join(opt.detectioh_ocl, folder, "labels"),
                                    conf=opt.conf_col, thresh=opt.thresh_col,
                                    save_path=os.path.join(opt.proofpath, file))

        if is_dtp and not result[file]['is_dtp']:
            result[file] = {"time":lower/30, "is_dtp":is_dtp}

    with open(os.path.join(opt.proofpath,'log.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print("LOG WAS SAVED")