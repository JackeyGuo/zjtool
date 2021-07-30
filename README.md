# python tools with onnx/tensorrt/onnxsim/vino

## TODO
- [x] onnxsim
- [x] onnx2trt
- [ ] valtrt
- [ ] onnx2vino


## Envirment

- docker: 18.06.1
- python: 3.7
- pytorch: 1.8.1
- onnx: 1.8.1
- onnx-simplifier: 0.3.6
- onnxruntime: 1.8.1
- tensorrt: 7.0.0.11

## onnx-tensorrt python tool

## Usage:

### Install

See [Install](docker/README.md)

### Run

+ container exec

```bash
nvidia-docker run -it --rm -v /path/to/your/resource:/data zjtool:0.1.4 \
onnx2trt \
-i /data/model.onnx \
-o /data/model.trt \
-f /data/imgs.txt \ # calibration images, one file per line, absolute path in container
-q int8 \
-s 1 3 224 224 \
-m 0.5 0.5 0.5 \
-v 0.25 0.25 0.25 \
-d
```

+ in container

```
nvidia-docker run -it --rm --entrypoint=/bin/bash -v /path/to/your/resource:/data zjtool:0.1.4

$root@bb7bcd8d70a6:/workspace# zjtool onnx2trt --help
Usage: zjtool onnx2trt [OPTIONS]

  Convert ONNX model to Tensorrt model.

Options:
  -i, --onnx-file TEXT            input onnx file  [required]
  -o, --engine-file TEXT          output engine file  [required]
  -f, --file-list TEXT            file list
  -q, --quant-mode [int8|fp16|fp32]
                                  quant mode
  -d, --shape-dynamic             dynamic shape
  -r, --resize-type [centerpad_resize]
                                  resize type [CenterPadResize/Cv2Resize/AlbuResize]
  -b, --border-value INTEGER...   bgr border value
  -s, --bchw-shape INTEGER...     input of bchw shape
  -m, --mean-value FLOAT...       mean and std value
  -v, --std-value FLOAT...        mean and std value
  -c, --calibrator-type [IInt8Calibrator2]
                                  calibrator type
  -p, --channel-order TEXT        channel order
  -u, --channel-first             channel first
  --help                          Show this message and exit.
```

## onnx-openvino python tool

## install

See [Install](zjtool/onnx2vino/README.md)

## gofastdfs

See [Install](zjtool/fastdfs/README.md)
​
### Run
```bash
Usage: zjtool fastdfs [OPTIONS]

  Download and Upload file to FastDFS server.

Options:

    上传文件：

    '-f' file       help='待上传或文件路径‘
    '-s' scene      help='场景(path为空时为默认根目录)'       default='default'
    '-t' tag        help='tag标识'                         default='None'
    '-e' encrypt    help='加密上传'

    下载文件：

    '-m' md5            help='文件md5'                      default='None'
    'u'  url            help='文件url'                      default='None'
    'j'  json           help='指定json配置文件'              default='None'
    'd'  dst            help='指定保存路径'                  default='.'
    '-s' scene          help='过滤不符合scene的文件'         default='None'
    '-t' tag            help='过滤不符合tag标识的文件'        default='None'
    '-b' branch         help='指定业务分支'                  default=None
    '-e' decrypt        help='下载后解密'
```

# onnxsim python tools

### Run
+ container exec

```
nvidia-docker run -it --rm -v /path/to/your/resource:/data:/data zjtool:0.1.4 onnxsim \
-i /data/model.onnx \
-o /data/model-sim.onnx
```

```bash
Usage: zjtool onnxsim [OPTIONS]

  Simplifier onnx with official onnxsim.

Options:
  -i, --onnx-file TEXT            input onnx file  [required]
  -o, --onnxsim-file TEXT         output onnxsim file  [required]
  -n, --check_n                   check output
  -s, --input-shape               useful when the input shape is dynamic
  -ds, --dynamic-input-shape      enables dynamic input shape support
  -p, --input-data-path           input data
  --help                          Show this message and exit.
```

# References

Appreciate the great work from the following repositories:
+ [afterimagex/zjtool](https://github.com/afterimagex/zjtool)
+ [daquexian/onnx-simplifier](https://github.com/daquexian/onnx-simplifier)
