import os
from dataclasses import dataclass
import json

# 假设这些模块和类已经在你的项目中定义好了
from critiq.workflow_deepseek import (
    PairEvaluator,
    Workflow,
    ZeroOneEvaluator
)

from critiq import (
    launch_sglang_openai_api_server,
    launch_vllm_openai_api_server,
)

## deepseek
APP_KEYS = [
]


## 豆包
doubao_APP_KEYS = [ 
]

## qwen 3
qwen_APP_KEYS =[
    "Bearer app-FlExJxxxxxxxxxxxx",
]
## deepseek


def main():
    # 初始化工作流
    workflow = Workflow(
        manager_args={
            "api_keys":  qwen_APP_KEYS,
            "base_url":'https://mify-be.pt.xiaomi.com/api/v1/workflows/run',
            "request_kwargs": {
                "temperature": 1.0,
            },
            
        },
        worker_args={"api_keys": qwen_APP_KEYS,
            "base_url":'https://mify-be.pt.xiaomi.com/api/v1/workflows/run',},
        worker_max_concurrent=50,
        init_criteria = [
        {
            "name": "功能对等性",
            "description": "功能对等性是指翻译后的方言在实际交流场景中的作用、语义和语用功能与原普通话（包括英文）句子完全一致。"
        },
        {
            "name": "语义完整性",
            "description": "语义完整性指方言翻译需完整、准确地传达普通话原句的信息，重点在于信息的完整保留。"
        },
        {
            "name": "语法规范性",
            "description": "语法规范性主要聚焦于句子结构的逻辑性，但判断时需结合目标方言的表达习惯和语义理解。要以目标方言中常见的、约定俗成的语法结构和表达方式为判断标准，只要方言表达在目标方言中有合理语义和使用习惯，就应视为符合语法规范，不能仅从普通话的结构逻辑去评判，也不能仅从表面结构逻辑判断。同时，判断时要独立于其他指标，纯粹从结构上对比与原句的契合度，不能受语义、表达习惯、语义对应性等其他因素干扰。例如，在某些方言中可能存在一些与普通话不同的语序或虚词用法，只要在该方言语境中有合理语义和使用习惯，就应判定为符合语法规范。又如，给出类似原句和不同结构的方言表达，再如普通话中存在英文文本时，方言应该保持对应的英文文本，而非英文对应的解释。仅从结构上判断其逻辑性，严格按照此要求进行判断，不将其他无关因素纳入考量范围。"
        },
        {"name":"专有名词译制惯例遵循度","description": "如普通话存在专有名词，目标方言对影视 IP、角色名等专有名词若有官方译制或约定俗成的译法，需严格沿用，不存在默认为高质量数据。"},
        {"name": "英文一致性", "description": "如果普通话出现英文文本时，方言应保持英文文本一致，不能对英文进行解释，如果普通话没有英文文本，则为高质量数据"},
        {"name":"文本一致性","description": "普通话对应的方言文本不应该出现对方言文字的解释、拼音和注释等多余内容，不出现则为高质量数据,英文属于高质量"},
        {"name":"符合小爱语音助手场景","description": "方言翻译不能太口语，需要符合小爱语音助手这样得场景"},

    ],
        n_criteria=8,
        manager_prompt= "生成普通话翻译成方言的评判标准",
        manager_prompt_postfix=None,
        worker_prompt=None
    )

    # 准备训练和验证数据集
    file_path = "../huayu_CritiQ/dataset/huayu_train_yue_0703.jsonl"
    # file_path = "./dataset/0701_badcase_train.jsonl"
    with open(file_path, "r", encoding="utf-8") as f:
        train_set = [line for line in f]
    train_set = [json.loads(line) for line in train_set]
    # 调用 optimize 方法
    output_dir = "./cmx_results/mify_qwen3_yue15"
    workflow.optimize(
        train_set=train_set,
        output_dir=output_dir,
        num_epochs=10,
        threshold=(0.5, 0.9),
        save_thought=False,
        max_retries=3
    )

    print("Optimize completed. Results saved to:", output_dir)


if __name__ == "__main__":
    main()