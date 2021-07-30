# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Copyright (C) 2020-Present, Pvening, Co.,Ltd.
#
# Licensed under the BSD 2-Clause License.
# You should have received a copy of the BSD 2-Clause License
# along with the software. If not, See,
#
#      <https://opensource.org/licenses/BSD-2-Clause>
#
# ------------------------------------------------------------


import click

from zjtool.fastdfs.main import fastdfs


@click.group()
@click.version_option(version='0.1.0')
def cli():
    pass


cli.add_command(fastdfs)


@cli.command()
@click.option('-i', '--onnx-file',
              help='input onnx file',
              type=str,
              required=True)
@click.option('-o', '--engine-file',
              help='output engine file',
              type=str,
              required=True)
@click.option('-f', '--file-list',
              help='file list',
              type=str)
@click.option('-q', '--quant-mode',
              help='quant mode',
              type=click.Choice(['int8', 'fp16', 'fp32']),
              default='int8')
@click.option('-d', '--shape-dynamic',
              help='dynamic shape',
              is_flag=True)
@click.option('-r', '--resize-type',
              help='resize type：CenterPadResize/Cv2Resize/AlbuResize',
              type=click.Choice(['CenterPadResize', 'Cv2Resize', 'AlbuResize']),
              default='CenterPadResize')
@click.option('-b', '--border-value',
              help='bgr border value',
              nargs=3,
              type=int,
              default=(0, 0, 0))
@click.option('-s', '--bchw-shape',
              help='input of bchw shape',
              nargs=4,
              type=int,
              default=(1, 3, 224, 224))
@click.option('-m', '--mean-value',
              help='mean and std value',
              nargs=3,
              type=float,
              default=(0.5, 0.5, 0.5))
@click.option('-v', '--std-value',
              help='mean and std value',
              nargs=3,
              type=float,
              default=(0.25, 0.25, 0.25))
@click.option('-c', '--calibrator-type',
              help='calibrator type',
              type=click.Choice(['IInt8Calibrator2']),
              default='IInt8Calibrator2')
@click.option('-p', '--channel-order',
              help='channel order',
              type=str,
              default='rgb')
@click.option('-u', '--channel-first',
              help='channel first',
              is_flag=True,
              default=True)
def onnx2trt(**kwargs):
    """Convert ONNX model to TensorRT model."""
    from zjtool.onnx2trt.convert import main_convert
    main_convert(kwargs)


@cli.command()
@click.option('-i', '--onnx-file',
              help='input onnx file',
              type=str,
              required=True)
@click.option('-o', '--output-file',
              help='output engine file',
              type=str,
              required=True)
@click.option('-f', '--file-list',
              help='file list',
              type=str)
@click.option('-q', '--quant-mode',
              help='quant mode',
              type=click.Choice(['int8', 'fp16', 'fp32']),
              default='int8')
@click.option('-d', '--shape-dynamic',
              help='dynamic shape',
              is_flag=True)
@click.option('-r', '--resize-type',
              help='resize type',
              type=click.Choice(['CenterPadResize', 'Cv2Resize']),
              default='CenterPadResize')
@click.option('-b', '--border-value',
              help='bgr border value',
              nargs=3,
              type=int,
              default=(0, 0, 0))
@click.option('-s', '--bchw-shape',
              help='input of bchw shape',
              nargs=4,
              type=int,
              default=(1, 3, 224, 224))
@click.option('-m', '--mean-value',
              help='mean and std value',
              nargs=3,
              type=float,
              default=(0.5, 0.5, 0.5))
@click.option('-v', '--std-value',
              help='mean and std value',
              nargs=3,
              type=float,
              default=(0.5, 0.5, 0.5))
def onnx2vino(**kwargs):
    """Convert ONNX model to OpenVINO model."""
    pass


@cli.command()
@click.option('-i', '--input-model', help='Input ONNX model')
@click.option('-o', '--output-model', help='Output ONNX model')
@click.option('-c', '--check-n', help='Check whether the output is correct with n random inputs', type=int, default=3)
@click.option(
    '-s', '--input-shape',
    help='The manually-set static input shape, useful when the input shape is dynamic. The value should be "input_name:dim0,dim1,...,dimN" or simply "dim0,dim1,...,dimN" when there is only one input, for example, "data:1,3,224,224" or "1,3,224,224". Note: you might want to use some visualization tools like netron to make sure what the input name and dimension ordering (NCHW or NHWC) is.',
    type=str, nargs='+')
@click.option('-ds', '--dynamic-input-shape',
              help='This option enables dynamic input shape support. "Shape" ops will not be eliminated in this case. Note that "--input-shape" is also needed for generating random inputs and checking equality. If "dynamic_input_shape" is False, the input shape in simplified model will be overwritten by the value of "input_shapes" param.')
@click.option(
    '-p', '--input-data-path',
    help='input data, The value should be "input_name1:xxx1.bin"  "input_name2:xxx2.bin ...", input data should be a binary data file.',
    type=str, nargs='+')
def onnxsim(**kwargs):
    """Simplifier onnx with official onnxsim."""
    from zjtool.onnxsim.simplifier import main_simplifier
    main_simplifier(kwargs)


def main():
    cli()


if __name__ == '__main__':
    main()
