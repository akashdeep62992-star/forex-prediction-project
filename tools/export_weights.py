"""Export the Keras .h5 models to .npz weight files used by numpy_rnn.py.

Run this once after retraining (needs TensorFlow installed locally):

    python tools/export_weights.py

It also checks that the NumPy forward pass matches Keras on random inputs.
"""
import json
import os
import sys

import numpy as np
from tensorflow import keras

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from numpy_rnn import NumpyRNNModel  # noqa: E402

SUPPORTED = {"LSTM", "GRU", "BatchNormalization", "Dense", "Dropout"}


def export(name):
    src = os.path.join(ROOT, "Models", f"{name}_model.h5")
    dst = os.path.join(ROOT, "Models", f"{name}_weights.npz")
    model = keras.models.load_model(src, compile=False)

    spec, arrays = [], {}
    for idx, layer in enumerate(model.layers):
        kind = type(layer).__name__
        if kind not in SUPPORTED:
            raise ValueError(f"{name}: unsupported layer {kind}")
        cfg = layer.get_config()
        if kind == "GRU" and not cfg.get("reset_after", True):
            raise ValueError("Only GRU(reset_after=True) is supported")
        if cfg.get("go_backwards"):
            raise ValueError("go_backwards is not supported")
        spec.append({
            "type": kind,
            "return_sequences": cfg.get("return_sequences", False),
            "activation": cfg.get("activation"),
            "epsilon": cfg.get("epsilon"),
        })
        for j, w in enumerate(layer.get_weights()):
            arrays[f"{idx}_{j}"] = w
    np.savez_compressed(dst, __spec__=json.dumps(spec), **arrays)

    # Verify against Keras
    x = np.random.default_rng(0).random((32,) + tuple(model.input_shape[1:]))
    expected = model.predict(x, verbose=0)
    got = NumpyRNNModel(dst).predict(x)
    diff = float(np.max(np.abs(expected - got)))
    print(f"{name}: saved {os.path.relpath(dst, ROOT)}  max |keras - numpy| = {diff:.2e}")
    if diff > 1e-4:
        raise SystemExit(f"{name}: NumPy output does not match Keras")


if __name__ == "__main__":
    for model_name in ("lstm", "gru"):
        export(model_name)
