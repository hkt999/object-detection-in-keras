import json
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from models import SSD300_VGG16_ORIGINAL
from data_generators import SSD_VOC_DATA_GENERATOR
from utils import generate_default_boxes_for_feature_map, match_bounding_boxes_to_default_boxes

# SSD300_VGG16_ORIGINAL()

with open("configs/ssd300_vgg16_original.json") as config_file:
    config = json.load(config_file)

image = cv2.imread("data/test.jpg")
image_height, image_width, _ = image.shape
image = cv2.resize(image, (300, 300))


scales = np.linspace(0.1, 0.9, 6)
sizes = [38, 19, 10, 5, 3, 1]

default_boxes_layer = generate_default_boxes_for_feature_map(
    feature_map_size=1,
    image_size=300,
    offset=[0.5, 0.5],
    scale=0.9,
    next_scale=1,
    aspect_ratios=[
        1.0,
        2.0,
        0.5
    ],
    variances=[
        0.1,
        0.1,
        0.2,
        0.2
    ],
    normalize_coords=True,
    extra_box_for_ar_1=True
)

default_boxes_layer[:, :, :, [0, 2]] *= 300
default_boxes_layer[:, :, :, [1, 3]] *= 300

xml_root = ET.parse("data/test.xml").getroot()
height_scale, width_scale = 300/image_height, 300/image_width
objects = xml_root.findall("object")

gt_truth_boxes = np.zeros((len(objects), 4))

for i, obj in enumerate(objects):
    name = obj.find("name").text
    bndbox = obj.find("bndbox")
    xmin = (int(bndbox.find("xmin").text) * width_scale)
    ymin = (int(bndbox.find("ymin").text) * height_scale)
    xmax = (int(bndbox.find("xmax").text) * width_scale)
    ymax = (int(bndbox.find("ymax").text) * height_scale)
    gt_truth_boxes[i] = [xmin, ymin, xmax, ymax]

default_boxes_layer = np.reshape(default_boxes_layer, (-1, 8))

default_boxes = default_boxes_layer.copy()
default_boxes[:, 0] = default_boxes_layer[:, 0] - (default_boxes_layer[:, 2] / 2)
default_boxes[:, 1] = default_boxes_layer[:, 1] - (default_boxes_layer[:, 3] / 2)
default_boxes[:, 2] = default_boxes_layer[:, 0] + (default_boxes_layer[:, 2] / 2)
default_boxes[:, 3] = default_boxes_layer[:, 1] + (default_boxes_layer[:, 3] / 2)


matched = match_bounding_boxes_to_default_boxes(
    gt_truth_boxes[:, :4],
    default_boxes[:, :4]
)

# for i in range(default_boxes_layer.shape[0]):
#     box = default_boxes_layer[i, :4]
#     box = box.astype(int)
#     cv2.circle(image, (box[0], box[1]), 2, (0, 0, 255), 1)
#     cv2.rectangle(image, (box[0] - (box[2] // 2), box[1] - (box[3] // 2)), (box[0] + (box[2] // 2), box[1] + (box[3] // 2)), (0, 255, 0), 2)

# for i in range(gt_truth_boxes.shape[0]):
#     box = gt_truth_boxes[i, :4]
#     box = box.astype(int)
#     cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)

for i, (y, x) in enumerate(zip(matched[0], matched[1])):
    gt_box = gt_truth_boxes[y, :4].astype(int)
    db_box = default_boxes[x, :4].astype(int)
    cv2.rectangle(image, (gt_box[0], gt_box[1]), (gt_box[2], gt_box[3]), (255 * i * 0.2, 255 * i * 0.4, 255 * i * 0.5), 2)
    cv2.rectangle(image, (db_box[0], db_box[1]), (db_box[2], db_box[3]), (255 * i * 0.2, 255 * i * 0.4, 255 * i * 0.5), 2)
    print(y, x)

# for i in range(default_boxes_layer.shape[0]):
#     for j in range(default_boxes_layer.shape[1]):
#         if i == 10 and j == 10:
#             for b in range(default_boxes_layer.shape[2]):
#                 box = default_boxes_layer[i, j, b, :4]
#                 box = box.astype(int)
#                 cv2.circle(image, (box[0], box[1]), 2, (0, 0, 255), 1)
#                 cv2.rectangle(image, (box[0] - (box[2] // 2), box[1] - (box[3] // 2)), (box[0] + (box[2] // 2), box[1] + (box[3] // 2)), (0, 255, 0), 2)
#                 print(box)

cv2.imshow("image", image)

if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()

# data_generator = SSD_VOC_DATA_GENERATOR(
#     samples=["data/test.jpg data/test.xml"],
#     config=config
# )

# limit = 1

# for i, (batch_x, batch_y) in enumerate(data_generator):
#     print(f"batch {i+1}")
#     for j in range(len(batch_x)):
#         print(f"-- item {j}")
#     if i >= limit:
#         break