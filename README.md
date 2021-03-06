# python tools with onnx/tensorrt/onnxsim/vino

This repo is mainly to do model conversion around onnx, for example: onnxsim, tensorrt or openvino, etc. 
This repo is still being updated. . . . .

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
???
### Run
```bash
Usage: zjtool fastdfs [OPTIONS]

  Download and Upload file to FastDFS server.

Options:

    ???????????????

    '-f' file       help='???????????????????????????
    '-s' scene      help='??????(path???????????????????????????)'       default='default'
    '-t' tag        help='tag??????'                         default='None'
    '-e' encrypt    help='????????????'

    ???????????????

    '-m' md5            help='??????md5'                      default='None'
    'u'  url            help='??????url'                      default='None'
    'j'  json           help='??????json????????????'              default='None'
    'd'  dst            help='??????????????????'                  default='.'
    '-s' scene          help='???????????????scene?????????'         default='None'
    '-t' tag            help='???????????????tag???????????????'        default='None'
    '-b' branch         help='??????????????????'                  default=None
    '-e' decrypt        help='???????????????'
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
