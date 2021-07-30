import argparse
import sys
import onnx  # type: ignore
import onnxsim
import numpy as np
import parser

def main_simplifier(opts):
    print("Simplifying...")

    if opts["dynamic_input_shape"] and opts["input_shape"] is None:
        raise RuntimeError(
            'Please pass "--input-shape" argument for generating random input and checking equality. Run "python3 -m onnxsim -h" for details.')
    if opts["input_shape"] is not None and not opts["dynamic_input_shape"]:
        print(
            "Note: The input shape of the simplified model will be overwritten by the value of '--input-shape' argument. Pass '--dynamic-input-shape' if it is not what you want. Run 'python3 -m onnxsim -h' for details.")
    input_shapes = dict()
    if opts["input_shape"] is not None:
        for x in opts["input_shape"]:
            if ':' not in x:
                input_shapes[None] = list(map(int, x.split(',')))
            else:
                pieces = x.split(':')
                # for the input name like input:0
                name, shape = ':'.join(
                    pieces[:-1]), list(map(int, pieces[-1].split(',')))
                input_shapes.update({name: shape})

    input_data_paths = dict()
    if opts["input_data_path"] is not None:
        for x in opts["input_data_path"]:
            pieces = x.split(':')
            name, data = ':'.join(pieces[:-1]), pieces[-1]
            input_data_paths.update({name: data})

    input_tensors = dict()
    if len(input_data_paths) > 0 and opts["input_shape"] is not None:
        for name in input_shapes.keys():
            input_data = np.fromfile(input_data_paths[name], dtype=np.float32)
            input_data = input_data.reshape(input_shapes[name])
            input_tensors.update({name: input_data})

    model_opt, check_ok = onnxsim.simplify(
        opts["input_model"],
        check_n=opts["check_n"],
        input_shapes=input_shapes,
        input_data=input_tensors,
        dynamic_input_shape=opts["dynamic_input_shape"])

    onnx.save(model_opt, opts["output_model"])

    if check_ok:
        print("Ok!")
    else:
        print("Check failed, please be careful to use the simplified model, or try specifying \"--skip-fuse-bn\" or \"--skip-optimization\" (run \"python3 -m onnxsim -h\" for details)")
        sys.exit(1)
