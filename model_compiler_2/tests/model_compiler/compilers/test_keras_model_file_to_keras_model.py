# Copyright 2019 ZTE corporation. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import subprocess  # nosec
import sys
from tempfile import NamedTemporaryFile
from unittest import TestCase

import tensorflow as tf
from tensorflow import keras

import model_compiler.compilers.keras_model_file_to_keras_model as compiler
from model_compiler.models.sources.keras_model_file import KerasModelFile


def _get_custom_objects_script(keras_line):
    return f"""import sys

{keras_line}


class MyLayer(keras.layers.Layer):
    def __init__(self, output_dim, **kwargs):
        super().__init__(**kwargs)

        self._output_dim = output_dim
        self._kernel = None

    def build(self, input_shape):
        try:
            input_shape = input_shape.as_list()
        except AttributeError:
            pass

        self._kernel = self.add_weight(name='kernel', shape=(input_shape[1], self._output_dim), initializer='uniform')

        super().build(input_shape)

    def call(self, inputs, **kwargs):
        return keras.backend.dot(inputs, self._kernel)

    def compute_output_shape(self, input_shape):
        return input_shape[0], self._output_dim

    def get_config(self):
        config = super().get_config()

        config['output_dim'] = self._output_dim

        return config


class SomeUnusedClass:
    pass


def main():
    model = keras.Sequential([keras.layers.Dense(units=16, input_shape=[8]),
                              MyLayer(output_dim=4)])

    model.save(sys.argv[1], include_optimizer=False)


if __name__ == '__main__':
    main()
""".encode()


class CompileSourceTestCase(TestCase):
    def test_compile_simple(self):
        with NamedTemporaryFile(suffix='.h5') as model_file:
            with tf.compat.v1.Session(graph=tf.Graph()):
                keras.Sequential([keras.layers.Dense(units=4, input_shape=[8])]).save(model_file.name)

            compiled = compiler.compile_source(KerasModelFile(model_path=model_file.name))

            self.assertIsInstance(compiled.model, keras.Model)
            self.assertEqual(len(compiled.model.layers), 1)

            self.assertIsInstance(compiled.session, tf.compat.v1.Session)

    def test_compile_with_custom_objects(self):
        for import_keras in ['from tensorflow import keras']:
            with NamedTemporaryFile(suffix='.py') as script_file, NamedTemporaryFile(suffix='.h5') as model_file:
                script_file.file.write(_get_custom_objects_script(import_keras))
                script_file.file.flush()

                subprocess.run(args=[sys.executable, script_file.name, model_file.name], check=True)  # nosec

                compiled = compiler.compile_source(KerasModelFile(model_path=model_file.name,
                                                                  script_path=script_file.name))

                self.assertIsInstance(compiled.model, keras.Model)
                self.assertEqual(len(compiled.model.layers), 2)

                self.assertIsInstance(compiled.session, tf.compat.v1.Session)
