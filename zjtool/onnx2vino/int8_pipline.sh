export CONTAINER_NAME=openvino_dev
export DOCKER_MOUNT_POINT=/home/xupeichao/ws/onnx2openvino/:/models  # 模型挂载目录

python int8_pipline.py \
--input /home/xupeichao/ws/deep-text-recognition-benchmark/export/saved_models_aug128_dim_iter_100000.pth/slpr_128x32_dim.onnx \
--shape "1,3,32,128" \
--mean "127.5,127.5,127.5" \
--scale "127.5,127.5,127.5" \
--data_path /home/xupeichao/ws/deep-text-recognition-benchmark/predata
