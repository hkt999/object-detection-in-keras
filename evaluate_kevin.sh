python evaluate.py \
/home/kevin/work/training_data/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/JPEGImages \
/home/kevin/work/training_data/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/Annotations \
/home/kevin/work/object-detection-in-keras/output/ssd300_mobinet_v2_pascal-voc-2007/model.h5 \
/home/kevin/work/training_data/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/ImageSets/Main/test.txt \
--label_maps=/home/kevin/work/object-detection-in-keras/label_maps.txt \
--output_dir=./output/evaluations/model.h5 \
--iou_threshold=0.5
