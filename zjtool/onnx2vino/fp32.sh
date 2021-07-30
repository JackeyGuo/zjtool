export CONTAINER_NAME=openvino_dev
export DOCKER_MOUNT_POINT=/home/xupeichao/ws/onnx2openvino/:/models  # 模型挂载目录

python fp32.py \
--input /home/xupeichao/ws/deep-text-recognition-benchmark/export/saved_models_aug128_iter_300000.pth/slpr_128x32_3w.onnx \
--shape "1,3,32,128" \
--mean "127.5,127.5,127.5" \
--scale "127.5,127.5,127.5"
