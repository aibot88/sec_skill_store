---
name: scitex-nn
description: PyTorch neural-network building blocks for neuroscience and signal processing. Differentiable filters (`BandPassFilter`, `BandStopFilter`, `HighPassFilter`, `LowPassFilter`, `GaussianFilter`, `DifferentiableBandPassFilter`) operate on 1D channels-first tensors. `Hilbert` provides differentiable Hilbert transform for analytic-signal extraction. Architecture blocks: `BNet` / `BNet_Res` (B-shaped backbone with optional residual connections), `BHead` (decoder head). Augmentation/regularization: `AxiswiseDropout`, `DropoutChannels`, `ChannelGainChanger`, `FreqGainChanger` (gain perturbation in time and frequency domains for SSL training). Drop-in replacement for hand-rolled `torch.nn.Conv1d` butterworth-init wrappers, scattered Hilbert implementations using `torch.fft`, and bespoke channel-dropout layers. Use whenever a model needs trainable filter banks, differentiable spectral features, or SSL-style time/frequency augmentation.
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-nn/src/scitex_nn/_skills/scitex-nn/SKILL.md
tags: [scitex-nn, scitex-package, pytorch, neural-network, dsp, neuroscience]
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-nn

PyTorch building blocks specialized for neuroscience / signal-processing
models — differentiable filters, Hilbert, B-shaped backbones, and
spectral augmentation.

## Differentiable filters

```python
from scitex_nn import BandPassFilter, BandStopFilter, GaussianFilter

bp = BandPassFilter(low=4.0, high=8.0, fs=1000.0, order=4)
y = bp(x)                       # x: (batch, channels, samples)
```

`DifferentiableBandPassFilter` learns `low`/`high` end-to-end (use when
the band of interest is itself a hyperparameter).

## Hilbert transform

```python
from scitex_nn import Hilbert
analytic = Hilbert()(x)          # x: (..., samples) → complex tensor
```

## Backbones

```python
from scitex_nn import BNet, BNet_Res, BNet_config_v1

cfg = BNet_config_v1(in_chans=64, out_chans=2, ...)
model = BNet(cfg)
```

`BNet_Res` adds residual connections; the same config dataclass works.

## Augmentation

- `AxiswiseDropout(p, axis)` — drops along a chosen axis (channel,
  time, frequency)
- `DropoutChannels(p)` — convenience wrapper
- `ChannelGainChanger(min_gain, max_gain)` — random per-channel gain
- `FreqGainChanger(...)` — same in frequency domain via FFT

These compose as plain `nn.Module`s — drop into a `nn.Sequential`.

## When to use

- ✅ Trainable / differentiable signal processing inside a model
- ✅ SSL-style time / frequency augmentation pipelines
- ✅ Replacing tens of lines of hand-rolled FIR/Butterworth init
- ❌ Classical (non-trainable) filtering — use `scipy.signal` or
  `scitex-dsp`

## See also

- `scitex-dsp` — non-trainable counterparts (numpy/scipy-backed)
- General skill `01_arch_06_local-state-directories.md` if model
  checkpoints / cache directories need a canonical location

<!-- EOF -->
