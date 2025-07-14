

# CritiQ: Mining Data Quality Criteria from Human Preferences

[![GitHub KYLN24/CritiQ](https://img.shields.io/badge/GitHub-CritiQ-blue?logo=github)](https:/。/github.com/KYLN24/CritiQ) [![arXiv.2502.19279](https://img.shields.io/badge/arXiv-2502.19279-red?logo=arxiv)](https://arxiv.org/abs/2502.19279) [![Hugging Face Paper Page](https://img.shields.io/badge/Paper%20Page-2502.19279-yellow?logo=huggingface)](https://huggingface.co/papers/2502.19279)

## Updates

<!-- - 
- **Upcoming**: 🤗 We will release the knowledge base for *CritiQ Flow* on Hugging Face Hub.
- **Upcoming**: 🤗 We will released the CritiQ Scorers for [code](https://huggingface.co/KYLN24/CritiQ-Scorer-Code), [math](https://huggingface.co/KYLN24/CritiQ-Scorer-Math), and [logic](https://huggingface.co/KYLN24/CritiQ-Scorer-Logic) on Hugging Face Hub. -->
- **2025-05-16**: 🎉 Our paper has been accepted to the main conference of **ACL 2025**.
- **2025-03-07**: 🛠️ We release the Python implementation of *CritiQ* on GitHub.
- **2025-02-26**: 📝 We published the preprint [*CritiQ: Mining Data Quality Criteria from Human Preferences*](https://arxiv.org/abs/2502.19279) on arXiv.

## Quick Start

### Installation

```bash
git clone https://github.com/KYLN24/CritiQ
cd CritiQ
pip install -e ".[vllm,train]"
```
### Usage

TODO. Refer to the paper for more details.

豆包和千问共用一个py文件，使用的api来源于cloudml中的模型广场，使用时请自行更换api和模型。非内部使用时，使用该文件进行调用

deepseek来源于mify，使用时请自行更换app_keys，记得挂载IAM，否则容易api余额不足。


train
```bash
python /critiq/scripts/train_mify.py
```

eval
```bash
python /critiq/scripts/annotation_mify.py
```


<!-- 
#### (Optional) Download the Knowledge Base

TODO

#### Prepare Data

TODO

#### Run CritiQ Flow

TODO

#### Agent Annotation

TODO

#### Train CritiQ Scorer

TODO

#### Score the Dataset

TODO

#### Perform Sampling -->
