import cv2
import numpy as np
import tensorflow as tf
import xml.etree.ElementTree as ET
from utils import generate_default_boxes_for_feature_map, match_gt_boxes_to_default_boxes


class SSD_VOC_DATA_GENERATOR(tf.keras.utils.Sequence):
    """ Data generator for training SSD networks using with VOC labeled format.
    Args:
    - samples: 
    - input_shape: 
    - batch_size: 
    - num_classes: 
    - shuffle: 
    - aspect_ratios: 
    - variances: 
    - extra_box_for_ar_1: 

    Returns:
    - 

    """

    def __init__(self, samples, config):
        self.samples = samples
        #
        self.batch_size = config["training"]["batch_size"]
        self.shuffle = config["training"]["shuffle"]
        self.data_dir = config["training"]["data_dir"]
        #
        self.input_shape = config["model"]["input_shape"]
        self.num_classes = config["model"]["num_classes"]
        self.extra_box_for_ar_1 = config["model"]["extra_box_for_ar_1"]
        self.normalize_coords = config["model"]["normalize_coords"]
        self.default_boxes_config = config["model"]["default_boxes"]
        self.indices = range(0, len(self.samples))
        #
        assert self.batch_size <= len(self.indices), "batch size must be smaller than the number of samples"
        assert self.input_shape[0] == self.input_shape[1], "input width should be equals to input height"
        self.input_size = min(self.input_shape[0], self.input_shape[1])
        self.input_template = self.__get_input_template()
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size

    def __getitem__(self, index):
        index = self.index[index * self.batch_size:(index + 1) * self.batch_size]
        batch = [self.indices[k] for k in index]
        X, y = self.__get_data(batch)
        return X, y

    def on_epoch_end(self):
        self.index = np.arange(len(self.indices))
        if self.shuffle == True:
            np.random.shuffle(self.index)

    def __get_input_template(self):
        scales = np.linspace(
            self.default_boxes_config["min_scale"],
            self.default_boxes_config["max_scale"],
            len(self.default_boxes_config["layers"])
        )
        mbox_conf_layers = []
        mbox_loc_layers = []
        mbox_default_boxes_layers = []
        for i, layer in enumerate(self.default_boxes_config["layers"]):
            layer_default_boxes = generate_default_boxes_for_feature_map(
                feature_map_size=layer["size"],
                image_size=self.input_shape[0],
                offset=layer["offset"],
                scale=scales[i],
                next_scale=scales[i+1] if i+1 <= len(self.default_boxes_config["layers"]) - 1 else 1,
                aspect_ratios=layer["aspect_ratios"],
                variances=self.default_boxes_config["variances"],
                normalize_coords=self.normalize_coords,
                extra_box_for_ar_1=self.extra_box_for_ar_1
            )
            layer_default_boxes = np.reshape(layer_default_boxes, (-1, 8))
            mbox_conf_layers.append(np.zeros((layer_default_boxes.shape[0], self.num_classes)))
            mbox_loc_layers.append(np.zeros((layer_default_boxes.shape[0], 4)))
            mbox_default_boxes_layers.append(layer_default_boxes)
        mbox_conf = np.concatenate(mbox_conf_layers, axis=0)
        mbox_loc = np.concatenate(mbox_loc_layers, axis=0)
        mbox_default_boxes = np.concatenate(mbox_default_boxes_layers, axis=0)
        template = np.concatenate([mbox_conf, mbox_loc, mbox_default_boxes], axis=-1)
        template = np.expand_dims(template, axis=0)
        return np.tile(template, (self.batch_size, 1, 1))

    def __get_data(self, batch):
        X = []
        y = self.input_template.copy()

        for sample_idx in batch:
            image_path, label_path = self.samples[sample_idx].split(" ")
            image = cv2.imread(image_path)  # read image in bgr format
            image_height, image_width, _ = image.shape
            height_scale, width_scale = self.input_size/image_height, self.input_size/image_width
            input_img = cv2.resize(image, (self.input_size, self.input_size))
            input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

            xml_root = ET.parse(label_path).getroot()
            objects = xml_root.findall("object")
            gt_truth_boxes = np.zeros((len(objects), 4))

            for i, obj in enumerate(objects):
                name = obj.find("name").text
                bndbox = obj.find("bndbox")
                xmin = int(bndbox.find("xmin").text) * width_scale
                ymin = int(bndbox.find("ymin").text) * height_scale
                xmax = int(bndbox.find("xmax").text) * width_scale
                ymax = int(bndbox.find("ymax").text) * height_scale
                gt_truth_boxes[i] = [xmin, ymin, xmax, ymax]

            matches = match_gt_boxes_to_default_boxes(
                gt_boxes=gt_truth_boxes,
                default_boxes=y[sample_idx, :, -8:-4] * self.input_size
            )

            X.append(input_img)
            # y.append(1)

        return X, y
