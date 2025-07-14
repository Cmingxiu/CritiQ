# CritiQ: Mining Data Quality Criteria from Human Preferences

[![GitHub KYLN24/CritiQ](https://img.shields.io/badge/GitHub-CritiQ-blue?logo=github)](https:/。/github.com/KYLN24/CritiQ) [![arXiv.2502.19279](https://img.shields.io/badge/arXiv-2502.19279-red?logo=arxiv)](https://arxiv.org/abs/2502.19279) [![Hugging Face Paper Page](https://img.shields.io/badge/Paper%20Page-2502.19279-yellow?logo=huggingface)](https://huggingface.co/papers/2502.19279)

## Updates

<!-- - 
- **Upcoming**: 🤗 We will release the knowledge base for *CritiQ Flow* on Hugging Face Hub.
- **Upcoming**: 🤗 We will released the CritiQ Scorers for [code](https://huggingface.co/KYLN24/CritiQ-Scorer-Code), [math](https://huggingface.co/KYLN24/CritiQ-Scorer-Math), and [logic](https://huggingface.co/KYLN24/CritiQ-Scorer-Logic) on Hugging Face Hub. -->

- 原始代码来源于 [CritiQ](https://github.com/KYLN24/CritiQ)，本项目在此基础上添加了对千问和豆包的调用，以及对mify的调用。
- **2025-05-16**: 🎉 Our paper has been accepted to the main conference of **ACL 2025**.
- **2025-03-07**: 🛠️ We release the Python implementation of *CritiQ* on GitHub.
- **2025-02-26**: 📝 We published the preprint [*CritiQ: Mining Data Quality Criteria from Human Preferences*](https://arxiv.org/abs/2502.19279) on arXiv.

## Quick Start

### Installation

```bash
git clone https://github.com/Cmingxiu/CritiQ.git
cd CritiQ
pip install -e ".[vllm,train]"
```
### 文件说明
```bash
CritiQ/
│
├── README.md
├── dataset/  #数据集存在位置
├── critiq/
│   ├── __init__.py
│   ├── _pycache__/
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── eval_mify.py  # mify评估调用
│   │   ├── eval_cloudml.py # cloudml 评估调用
│   │   ├── annotation.py # 本地模型调用
│   │   ├── reward_predict_vllm.py
│   │   ├── reward_predict.py # score评分器评估
│   │   ├── train_mify.py  # mify训练调用
│   │   ├── train_cloudml.py # cloudml 训练调用
│   │   ├── train_reward.py # 训练socre评分器（本地大模型）
│   ├── agent_mify.py # mify api调用
│   ├── agent.py # 本地模型和cloudml api调用
│   ├── critiq_excel.py # crtiq结果转为表格
│   ├── create_dataset.py # 表格数据到数据集建立
│   ├── crit.txt # 一些标准样例
│   ├── critiq_select_content.py # 筛选翻译模型的训练数据
│   ├── critiq_select_soundbox.py # 筛选翻译模型的训练数据
│   ├── evaluator_mify.py # mify的评估流程
│   ├── evaluator.py # 本地和cloudml的评估流程
│   ├── i18n.py  # promote配置文件
│   ├── json_add.py # 将code=0的新增数据添加到code=1的目录下
│   ├── utils.py # 一些判断函数
│   ├── workflow_mify.py # mify标准更新流程
└── └── workflow.py # 本地模型和clouml标准更新流程
```

### Usage

Usage

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
