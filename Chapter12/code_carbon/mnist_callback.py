"""
This sample code sis taken from https://github.com/mlco2/codecarbon/blob/master/examples/
It shows how to use CodeCarbon as a Keras Callback
to compute the emissions in the overall training process
"""

import tensorflow as tf
from tensorflow.keras.callbacks import Callback

from codecarbon import EmissionsTracker

class CodeCarbonCallBack(Callback):
    def __init__(self, codecarbon_tracker):
        self.codecarbon_tracker = codecarbon_tracker
        pass

    def on_epoch_end(self, epoch, logs=None):
        self.codecarbon_tracker.flush()


mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])

tracker = EmissionsTracker()
tracker.start()
codecarbon_cb = CodeCarbonCallBack(tracker)
model.fit(x_train, y_train, epochs=10, callbacks=[codecarbon_cb])
emissions: float = tracker.stop()
print(f"Emissions: {emissions} kg")
