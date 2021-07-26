python train.py \
configs/ssd300_mobilenetv3.json \
/home/kevin/work/datasets/VOC2007/voctrainval_06-nov-2007/VOCdevkit/VOC2007/JPEGImages \
/home/kevin/work/datasets/VOC2007/voctrainval_06-nov-2007/VOCdevkit/VOC2007/Annotations \
--training_split=/home/kevin/work/datasets/VOC2007/voctrainval_06-nov-2007/VOCdevkit/VOC2007/ImageSets/Main/train.txt \
--validation_split=/home/kevin/work/datasets/VOC2007/voctrainval_06-nov-2007/VOCdevkit/VOC2007/ImageSets/Main/val.txt \
--label_maps=/home/kevin/work/datasets/VOC2007/label_maps.txt \
--learning_rate=0.001 \
--epochs=100 \
--batch_size=3 \
--shuffle=True \
--augment=True \
--output_dir=output/ssd300_mobinet_v3_pascal-voc-2007

