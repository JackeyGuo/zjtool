# onnx-tensorrt docker envirment

## docker pull

```bash
docker pull jackeyguo/onnx-tensorrt:cuda10.2-cudnn7-tensorrt7.0.0.11-ubuntu18.04-py37
```

## docker build

```bash
cd /tmp && mkdir build_docker && cd build_docker
cp ${path/to/repo}/zjtool/docker/onnx-tensorrt7.0-py37-cuda10.2.Dockerfile .
cp ${path/to/downlaod TensorRT-*.tar.gz}/TensorRT-7.0.0.11.*.tar.gz .
git clone --recurse-submodules https://github.com/onnx/onnx-tensorrt.git -b 7.0
docker build -f onnx-tensorrt7.0-py37-cuda10.2.Dockerfile --tag=onnx-tensorrt:10.2-7.0 .
```

# zjtool docker envirment

## docker pull

```bash
docker pull jackeyguo/onnx-tensorrt:zjtool-0.1.4-tensorrt7.0.0.11-ubuntu18.04-py36-zh
```

## docker build

```bash
docker build -f zjtool-tensorrt7.Dockerfile --tag=zjtool:0.1.4 .
```