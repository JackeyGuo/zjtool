FROM jackeyguo/onnx-tensorrt:cuda10.2-cudnn7-tensorrt7.0.0.11-ubuntu18.04-py37

RUN cd /tmp && \
    git clone https://github.com/JackeyGuo/zjtool.git && \
    cd zjtool && python setup.py install && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
    rm -rf ~/.cache/pip

CMD ["--help"]
ENTRYPOINT ["zjtool"]