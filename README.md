# TC-π0.5

Three-layer spatiotemporal graph conditioning for π0.5: global state and preceding task tokens enter the VLM prefix; local interaction and latent subgoal tokens enter the action expert. The current release is the exact full-fine-tuned `cook_hot_dogs` step5000 model evaluated on 2026-10-25.

## Results

BEHAVIOR public-test instances 301–310; action seed42; 32-action chunks; official termination and Q. TC-π0.5 uses RGB + Oracle graphs and full fine-tuning; the reference is frozen RGB PT50.

|Model|Success|Mean Q|
|---|---:|---:|
|π0.5-behaviour-base (PT50)|2/10 (20%)|0.20|
|TC-π0.5, cook_hot_dogs, step5000|5/10 (50%)|0.55|

|Instance|PT50 success|PT50 Q|TC-π0.5 success|TC-π0.5 Q|
|---|---:|---:|---:|---:|
|301|0|0.0|0|0.0|
|302|1|1.0|1|1.0|
|303|0|0.0|1|1.0|
|304|0|0.0|1|1.0|
|305|0|0.0|0|0.0|
|306|0|0.0|1|1.0|
|307|0|0.0|0|0.0|
|308|0|0.0|1|1.0|
|309|0|0.0|0|0.5|
|310|1|1.0|0|0.0|

Reproduction tag: `cook-hot-dogs-step5000`. Check out this tag to reproduce the released code after future updates.

## Run

Linux, Python3.11, NVIDIA GPU. The inference server does not require Isaac Sim.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/prepare_env.py
python tools/download_weights.py --output weights
python tools/verify.py --weights weights
python tools/serve.py --weights weights --port 18817
```

The relocated source tree has passed a GPU inference smoke test with the published model hash. In another terminal, test the inference interface:

```bash
source .venv/bin/activate
python tools/smoke_client.py --port 18817
```

For a real episode, install BEHAVIOR/Isaac and its assets separately, and use its Python environment with `numpy`, `msgpack`, `websockets` and Pillow. Forward port18817 if the simulator is on another machine. Then run:

```bash
python tools/run_episode.py --instance 308 --port 18817 --output runs/instance308
```

A pinned robot URDF and nominal geometry metadata are included; Isaac Sim and BEHAVIOR scene assets are external. The actor obtains actual joint/proprioceptive feedback, three onboard RGB views, task-scoped Oracle object states and nominal geometry. Expected action output is32×23. `examples/graph_snapshot.json` is an interface fixture, not a task demonstration.

## Reproduction identity

- Tested graph/model/runtime sources and upstream OpenPI-Comet sources are preserved byte-for-byte. Five exact Transformers4.53.2 replacement files are installed by `prepare_env.py`.
- Weight assets, tokenizer, normalizer and skill candidate table are pinned by SHA256; the Hugging Face revision is pinned in `reproduction/release_manifest.json`.
- The portable launcher changes only the runtime copy of the historical checkpoint-location field. Original metadata and all tensor bytes remain unchanged. Original inference/checkpoint validation is used.
- Training: full backbone + graph modules, no LoRA;4970 formal updates ×48 sequences, approximately4.613 epochs. The user selected cumulative step5000 before the five-epoch budget completed.
- Global8 / Task4 / Local8 / Subgoal2 tokens; graph hidden256; local history≤16 updates; training2-chunk BPTT, inference episode memory. TaskManager is procedural. Candidate selection uses23 fixed slots,22 legal in this release.

## Layout and weights

`src/tgr`: tested modules; `code`: pinned upstream source; `deployment`: original evaluated actor; `tools`: portable launch/download/verification; `reproduction`: hashes and results.

Weights: [Songyuan666/TC-pi0.5](https://huggingface.co/Songyuan666/TC-pi0.5).

```text
cook_hot_dogs/step5000/      # TC-π0.5 full model + original metadata
pi0.5-behaviour-base/        # unchanged 50-task PT50 base, config and normalization
common/                    # bundled PaliGemma tokenizer
```

Upstream code: [OpenPI-Comet](https://github.com/mli0603/openpi-comet), commit `4bb2aa7bb2da32614cac128ebb4b2f96eb66e5b5`. Base weights: `sunshk/openpi_comet_pytorch`, revision `5a489fe50fdc8e256533c8c611dfd60c247520cf`. Dataset: `behavior-1k/2025-challenge-demos`. Upstream code licenses and model/asset usage terms remain applicable.
