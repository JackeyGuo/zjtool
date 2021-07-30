# git clone --recurse-submodules https://github.com/onnx/onnx-tensorrt.git -b 7.0
# docker build -f onnx-tensorrt7.0-py37-cuda10.2.Dockerfile --tag=onnx-tensorrt:10.2-7.0 .

FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04
MAINTAINER guofeng@fosun.com
ARG TENSORRT_VERSION=7.0.0.11
ARG PY3_VERSION=37

COPY sources.list /etc/apt/
COPY . /tmp

RUN /bin/bash /tmp/Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -p /home/anaconda3
ENV PATH=/home/anaconda3/bin:$PATH
ENV http_proxy=http://172.16.17.164:3128
ENV https_proxy=http://172.16.17.164:3128

# Install package dependencies
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    rm /etc/apt/sources.list.d/* && \
    apt-get update -y && \
    apt-get install -y tzdata locales libglib2.0-dev libsm6 libxrender1 libxext6 \
	build-essential autoconf automake libtool pkg-config ca-certificates wget \
	git libgl1-mesa-glx libprotobuf-dev protobuf-compiler swig vim htop zip \
	gcc g++ libxrender-dev curl bzip2 && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && \
    pip config set install.trusted-host mirrors.aliyun.com && \
    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* && \
	rm -rf ~/.cache/pip
	
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

RUN pip install scikit-build==0.11.1 \
	opencv-python==4.4.0.46 \
	onnx==1.8.1 \
	pillow==8.0.1 \
	albumentations==1.0.1 \
	scikit-learn==0.22.1 \
	onnx-simplifier==0.3.6 \
	onnxruntime==1.8.1 --no-cache-dir && \
	pip install /tmp/torch-1.8.1+cu102-cp37-cp37m-linux_x86_64.whl --no-cache-dir && \
	pip install	/tmp/torchvision-0.9.1+cu102-cp37-cp37m-linux_x86_64.whl --no-cache-dir && \
	rm -rf ~/.cache/pip

WORKDIR /tmp

RUN wget https://github.com/Kitware/CMake/releases/download/v3.15.7/cmake-3.15.7-Linux-x86_64.sh && \
    chmod +x cmake-3.15.7-Linux-x86_64.sh && \
    ./cmake-3.15.7-Linux-x86_64.sh --prefix=/usr/local --exclude-subdir --skip-license && \
    rm ./cmake-3.15.7-Linux-x86_64.sh && \
	# Install TensorRT
	tar -xvf TensorRT-${TENSORRT_VERSION}.*.tar.gz && \
    cd TensorRT-${TENSORRT_VERSION}/ && \
    cp lib/lib* /usr/lib/x86_64-linux-gnu/ && \
    rm /usr/lib/x86_64-linux-gnu/libnv*.a && \
    cp include/* /usr/include/x86_64-linux-gnu/ && \
    cp bin/* /usr/bin/ && \
    mkdir /usr/share/doc/tensorrt && \
    cp -r doc/* /usr/share/doc/tensorrt/ && \
    mkdir /usr/src/tensorrt && \
    cp -r samples /usr/src/tensorrt/  && \
    pip install python/tensorrt-${TENSORRT_VERSION}-cp${PY3_VERSION}-none-linux_x86_64.whl && \
    pip install uff/uff-*-py2.py3-none-any.whl && \
	rm -rf ~/.cache/pip
	
# Build the library
ENV ONNX2TRT_VERSION 0.1.0

WORKDIR /tmp/onnx-tensorrt

RUN rm -rf build/ && \
    mkdir -p build && \
    cd build && \
    cmake -DCUDA_INCLUDE_DIRS=/usr/local/cuda/include/ .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd .. && \
    sed -i "22i#define TENSORRTAPI" NvOnnxParser.h && \
    python setup.py build && \
    python setup.py install && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
	rm -rf ~/.cache/pip
	
WORKDIR /home