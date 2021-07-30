
# ONNX2VINO

onnx模型一键转换openvino量化后模型

安装启动docker
```
sudo docker pull openvino/ubuntu18_dev
sudo docker run -itd --name openvino_dev -u root -v /home/xupeichao/ws/onnx2openvino/:/models --privileged=true openvino/ubuntu18_dev /bin/bash
```

模型转换
```
export CONTAINER_NAME=openvino_dev
export DOCKER_MOUNT_POINT=/home/xupeichao/ws/onnx2openvino/:/models  # 模型挂载目录

python int8_pipline.py \
--input /home/xupeichao/ws/deep-text-recognition-benchmark/export/saved_models_aug128_iter_300000.pth/slpr_128x32_3w.onnx \
--shape "1,3,32,128" \
--mean "127.5,127.5,127.5" \
--scale "127.5,127.5,127.5" \
--data_path /home/xupeichao/ws/deep-text-recognition-benchmark/predata
```