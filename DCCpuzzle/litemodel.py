import numpy as np
import tensorflow as tf
from timeit import default_timer as timer

# NO MODIFICAR

def from_file(model_path):
    return LiteModel(tf.lite.Interpreter(model_path=model_path))

def from_keras_model(model_path):
    kmodel = tf.keras.models.load_model(model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(kmodel)
    tflite_model = converter.convert()
    return LiteModel(tf.lite.Interpreter(model_content=tflite_model))

class LiteModel:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.interpreter.allocate_tensors()
        input_det = self.interpreter.get_input_details()[0]
        output_det = self.interpreter.get_output_details()[0]
        self.input_index = input_det["index"]
        self.output_index = output_det["index"]
        self.input_shape = input_det["shape"]
        self.output_shape = output_det["shape"]
        self.input_dtype = input_det["dtype"]
        self.output_dtype = output_det["dtype"]
        
    def predict(self, inp):
        inp = inp.astype(self.input_dtype)
        count = inp.shape[0]
        out = np.zeros((count, self.output_shape[1]), dtype=self.output_dtype)
        for i in range(count):
            self.interpreter.set_tensor(self.input_index, inp[i:i+1])
            self.interpreter.invoke()
            out[i] = self.interpreter.get_tensor(self.output_index)[0]
        return out
    
    def predict_single(self, inp):
        """ Like predict(), but only for a single record. The input data can be a Python list. """
        inp = np.array(inp, dtype=self.input_dtype).reshape(1, -1)
        self.interpreter.set_tensor(self.input_index, inp)
        self.interpreter.invoke()
        out = self.interpreter.get_tensor(self.output_index)
        # values = out[0]
        # h = np.argmax(values)
        # return h
        return out[0]