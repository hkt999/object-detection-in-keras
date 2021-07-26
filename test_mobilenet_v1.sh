python test.py \
/home/kevin/work/datasets/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/ImageSets/Main/test.txt \
/home/kevin/work/datasets/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/JPEGImages \
/home/kevin/work/datasets/VOC2007/voctest_06-nov-2007/VOCdevkit/VOC2007/Annotations \
configs/ssd300_mobilenetv1.json \
./output/ssd300_mobinet_v1_pascal-voc-2007/model.h5 \
--label_maps=/home/kevin/work/datasets/VOC2007/label_maps.txt \
--output_dir=./output/test/model.h5 \
--num_predictions=10
