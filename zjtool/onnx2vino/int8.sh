export CONTAINER_NAME=openvino_dev
export DOCKER_MOUNT_POINT=/home/xupeichao/ws/onnx2openvino/:/models  # 模型挂载目录

python int8.py \
--model_path /home/xupeichao/ws/onnx2openvino/slpr_128x32_3w \
--data_path /home/xupeichao/ws/deep-text-recognition-benchmark/predata \
--nocopy
