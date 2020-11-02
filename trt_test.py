import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import tensorrt as trt

# logger to capture errors, warnings, and other information during the build and inference phases
TRT_LOGGER = trt.Logger()

def build_engine(onnx_file_path):
    # initialize TensorRT engine and parse ONNX model
    #network_creation_flag = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_PRECISION)
    network_creation_flag = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(network_creation_flag)
    parser = trt.OnnxParser(network, TRT_LOGGER)
    
    # parse ONNX
    with open(onnx_file_path, 'rb') as model:
        print('Beginning ONNX file parsing')
        if not parser.parse(model.read()):
            print('ERROR: Failed to parse the ONNX file.')
            for error in range(parser.num_errors):
                print(parser.get_error(error))
    print('Completed parsing of ONNX file')

    print(network.num_layers)
    last_layer = network.get_layer(network.num_layers - 1)
    # Check if last layer recognizes it's output
    if not last_layer.get_output(0):
        # If not, then mark the output using TensorRT API
        network.mark_output(last_layer.get_output(0))

    # allow TensorRT to use up to 1GB of GPU memory for tactic selection
    builder.max_workspace_size = 1 << 30
    # we have only one image in batch
    builder.max_batch_size = 1
    # use FP16 mode if possible
    if builder.platform_has_fast_fp16:
        builder.fp16_mode = True

    # generate TensorRT engine optimized for the target platform
    print('Building an engine...')
    engine = builder.build_cuda_engine(network)
    context = engine.create_execution_context()
    print("Completed creating Engine")

    with open('test.trt', 'wb') as f:
        f.write(engine.serialize())

    return engine, context

def main():
    engine, context = build_engine('yolov4_1_3_416_416_static.onnx')

if __name__ == "__main__":
    main()