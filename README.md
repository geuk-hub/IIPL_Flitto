## Introduction

IIPL_Flitto is a comprehensive speech and text processing toolkit. This repository provides a collection of modules and scripts for advanced speaker diarization, speech enhancement modeling, speech-to-text (STT), text-to-speech (TTS) and text processing. The toolkit is designed to facilitate research and development in automatic speech recognition (ASR), speaker identification, and natural language processing (NLP) tasks.

## Environment

- **OS**: Ubuntu 24.04.2
- **CUDA Toolkit**: 11.7
- **GPU Driver**: NVIDIA-SMI 570.144 (CUDA Version 12.8)

## Install
1. Clone this repository and navigate to IIPL_Flitto folder

```
git clone https://github.com/geuk-hub/IIPL_Flitto.git
cd IIPL_Flitto
```


2. Install Package

```
conda create --name IIPL_Flitto python=3.9
conda activate IIPL_Flitto

pip install --upgrade "pip<24.1"
cd DiarizeNet && pip install -r requirements.txt
```


3. Install additional packages

```
pip install Cython librosa pesq pystoi pydub tqdm toml colorful mir_eval torch_complex "numpy<2" "accelerate<1.0.0" ffmpeg --no-deps jieba Mecab pkuseg

conda install -c conda-forge compilers
pip install pkuseg nlptutti transformers soynlp

pip install -U openai-whisper
pip install openai
```


## Download checkpoints & data

Download the [pre-trained DiarizeNet checkpoint](https://www.dropbox.com/scl/fo/uyer0669wfhpvm055v5mf/ACbFAIbVxQbScEPlhhioL0A?rlkey=0hndtmi059oh2r5bh51i0q1op&st=ix16crxu&dl=0).

Download the [AdaptiVoice Model checkpoint](https://www.dropbox.com/scl/fo/2tifgu6mrwo0akgrn3din/AO5Gdhkg0L90ky0goTbepzI?rlkey=1wlpaknwo8zcmg35ac6fhj1jz&st=apdxg900&dl=0).

Download the [Machine Translation Model checkpoint](https://www.dropbox.com/scl/fo/3xle2g3505iydwbw6yqg7/APcyGLXHwL83A2Y3Lu_GaZU?rlkey=i36di9snedlj45vttk6nd0zw9&st=sdhgg06z&dl=0).

Download the [Error Correction Model checkpoint](https://www.dropbox.com/scl/fo/rsl0xailbxcoeiz1ebf5g/AOh-MttVZHLOsO8BH7dc7ZA?rlkey=lta539u6qrqovke5ndodtfsmu&st=3xh1n9xr&dl=0).

Download the [TTA Test Dataset](https://www.dropbox.com/scl/fi/zeps24kl7rgugpjdi9yqd/TTA_test_wer_cer_llm_acc.zip?rlkey=xdjxdvfgye4wjjyix1i4ot5rf&st=34rxda79&dl=0).

## TTA_test: WER/CER/LLM-based acc

Before running the following script, make sure to configure the following environment variables:

- **LANG**: Choose one language from KR (Korean), EN (English), CN (Chinese), or JP (Japanes).
- **ROOT**: Set this to the full path of your `IIPL_Flitto` repository.
- **DIARIZENET_CHECKPOINT**: Set this to the full path of your `DiarizeNet` checkpoint folder (the directory where you downloaded the DiarizeNet checkpoint).
- **OPENAI_API_KEY**: Provide your OpenAI API key

- **TTA Test Dataset**: Put your TTA Test Dataset files into `TTA_test/wer_cer_llm_based_acc_data` folder.
- **{LANG}_wav.scp**: Ensure that the {LANG}_wav.scp file inside TTA_test/wer_cer_llm_based_acc_data/{LANG} contains correct audio paths.

```
bash TTA_test/wer_cer_llm_based_acc.sh
```

## TTA_test: crossview-AP

1. Install Package

```
conda create -n adaptivoice python=3.9
conda activate adaptivoice

cd AdaptiVoice
pip install -r requirements.txt
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
conda install -c conda-forge ffmpeg
```

2. run

Before running the following script, make sure to configure the following environment variables:
- **root**: Set this to the full path of your `IIPL_Flitto` repository.
- **Crossview-AP_ckpt**: Put your CrossView-AP checkpoint files into `crossview-ap` folder.
- **Crossview-AP_datasets**: Put your CrossView-AP datasetse files into `crossview-ap` folder.
  
```
python metric/crossview-ap/code/evaluate_all.py
```

## TTA_test: BLEU/COMET

1. Install Package

```
conda create -n mt python=3.9
conda activate mt

cd Text_Processing/Machine_Translation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install numpy regex sacrebleu tensorboard matplotlib pandas cython setuptools pyarrow sacremoses tensorboardX unbabel-comet
pip install pip==23.3.1
conda install -c conda-forge gxx_linux-64
pip install --editable ./
conda install -c nvidia cuda-toolkit=11.8 cudatoolkit-dev=11.8
```

2. run

Before running the following script, make sure to configure the following environment variables:

- **root**: Set this to the full path of your `IIPL_Flitto` repository.
- **machin_translation_ckpt**: Set this to the full path of your `Machine Translation` checkpoints folder.
  
```
bash metric/bleu_comet.sh
```

### Error Correction

1. Install Package

```
conda create -n ec python=3.12
conda activate ec

pip install unsloth hgtk
```

2. run

Before running the following script, make sure to configure the following environment variables:

- **root**: Set this to the full path of your `IIPL_Flitto` repository.
- **model_path**: Set this to the full path of your `Error Correction` checkpoints folder.
  
```
python Text_Processing/Error_Correction/LLM_grammer_inference.py
```
