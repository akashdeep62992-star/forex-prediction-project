"""Lightweight NumPy inference for the app's Keras LSTM/GRU models.

TensorFlow alone needs ~400 MB of RAM, which does not fit on small hosting
plans. The models only need a forward pass, so their weights are exported
once to .npz files (see tools/export_weights.py) and run here with NumPy.

Supported layers (Keras semantics): LSTM, GRU (reset_after=True),
BatchNormalization (inference mode), Dense, Dropout (no-op at inference).
"""
import json

import numpy as np


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _lstm(x, kernel, recurrent, bias, return_sequences):
    # Keras gate order: input, forget, cell, output
    batch, steps, _ = x.shape
    units = recurrent.shape[0]
    h = np.zeros((batch, units))
    c = np.zeros((batch, units))
    xw = x @ kernel + bias
    outputs = []
    for t in range(steps):
        z = xw[:, t] + h @ recurrent
        i = _sigmoid(z[:, :units])
        f = _sigmoid(z[:, units:2 * units])
        g = np.tanh(z[:, 2 * units:3 * units])
        o = _sigmoid(z[:, 3 * units:])
        c = f * c + i * g
        h = o * np.tanh(c)
        if return_sequences:
            outputs.append(h)
    return np.stack(outputs, axis=1) if return_sequences else h


def _gru(x, kernel, recurrent, bias, return_sequences):
    # Keras gate order: update (z), reset (r), candidate (h); reset_after=True
    batch, steps, _ = x.shape
    units = recurrent.shape[0]
    h = np.zeros((batch, units))
    xw = x @ kernel + bias[0]
    outputs = []
    for t in range(steps):
        hr = h @ recurrent + bias[1]
        xt = xw[:, t]
        z = _sigmoid(xt[:, :units] + hr[:, :units])
        r = _sigmoid(xt[:, units:2 * units] + hr[:, units:2 * units])
        cand = np.tanh(xt[:, 2 * units:] + r * hr[:, 2 * units:])
        h = z * h + (1.0 - z) * cand
        if return_sequences:
            outputs.append(h)
    return np.stack(outputs, axis=1) if return_sequences else h


class NumpyRNNModel:
    """Drop-in replacement for keras Model.predict on the exported weights."""

    def __init__(self, path):
        data = np.load(path, allow_pickle=False)
        self.layers = json.loads(str(data["__spec__"]))
        self.weights = {k: data[k].astype(np.float64) for k in data.files if k != "__spec__"}

    def _w(self, idx, n):
        return [self.weights[f"{idx}_{j}"] for j in range(n)]

    def predict(self, x, verbose=0, batch_size=None):
        out = np.asarray(x, dtype=np.float64)
        for idx, layer in enumerate(self.layers):
            kind = layer["type"]
            if kind == "LSTM":
                out = _lstm(out, *self._w(idx, 3), layer["return_sequences"])
            elif kind == "GRU":
                out = _gru(out, *self._w(idx, 3), layer["return_sequences"])
            elif kind == "BatchNormalization":
                gamma, beta, mean, var = self._w(idx, 4)
                out = (out - mean) / np.sqrt(var + layer["epsilon"]) * gamma + beta
            elif kind == "Dense":
                kernel, bias = self._w(idx, 2)
                out = out @ kernel + bias
                if layer["activation"] == "relu":
                    out = np.maximum(out, 0.0)
                elif layer["activation"] not in ("linear", None):
                    raise ValueError(f"Unsupported activation: {layer['activation']}")
            elif kind == "Dropout":
                continue
            else:
                raise ValueError(f"Unsupported layer: {kind}")
        return out
