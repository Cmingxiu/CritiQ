import os
from dataclasses import dataclass
import json

# 假设这些模块和类已经在你的项目中定义好了
from critiq import (
    PairEvaluator,
    Workflow,
    ZeroOneEvaluator,
    launch_sglang_openai_api_server,
    launch_vllm_openai_api_server,
)



def main():
    # 初始化工作流
    workflow = Workflow(
        manager_args={
            "model": "Doubao-pro-32k",
            "api_keys": '3v6olsd5KgUev00JrPSHiN95Lg4txxxxxxxxxxxxxxx',
            "base_url":"http://ai-llm.cloudml.ai.srv/cloudml/v1",
            "request_kwargs": {
                "temperature": 1.0,
            },
            
        },
        worker_args={"model": "Doubao-pro-32k","api_keys": '3v6olsd5KgUev00JrPSHiN95Lg4txxxxxxxxxxxxxxx',
            "base_url":"http://ai-llm.cloudml.ai.srv/cloudml/v1",},
        worker_max_concurrent=10,
        init_criteria = [
        {
            "name": "准确性",
            "description": "普通话(包括英文）和方言表达意思总体保持一致，需要将方言转为对应普通话1，比较是否和原普通话的意思一致。"
        },
        {
            "name": "功能对等性",
            "description": "功能对等性是指翻译后的方言在实际交流场景中的作用、语义和语用功能与原普通话（包括英文）句子完全一致。"

        },
        {
            "name": "书写规范一致性",
            "description": "本指标评估文本是否符合权威方言书面规范，具体要求：1.优先采用《现代汉语方言大词典》等官方标准确定的用字；2.专有名词、技术术语及外来词保留原始书写形式；3.区分口语表达与书面规范，允许采用《香港增補字符集》等区域标准认可的方言俗字；4.当方言无明确对应词时应保持原词结构完整性；5.禁止因口语特征随意增删汉字笔画或使用同音替代字，如品牌名需原样保留。书面规范优先级排序：国家标准＞区域标准＞领域惯例＞口语转化需求。",
      
        },
        {
            "name": "用词恰当性",
            "description": "用词恰当性的核心是所选词汇要准确表达普通话（包括英文）原句的原意，不能仅以是否体现方言特色来判断。"
  
        },
        {
            "name": "简洁性",
            "description": "在保证准确传达原句意思、功能对等和语义完整的基础上，结合目标方言常见表达习惯、具体语境和原句语义，考量表达的简洁程度。若原普通话表达语义明确，保留原表达也可视作简洁，增加介词也属于简洁性。"
        },
        {
            "name": "语义完整性",
            "description": "语义完整性指方言翻译需完整、准确地传达普通话原句的信息，重点在于信息的完整保留，不涉及方言特色、方言翻译要求、词汇形式、精准度、表达习惯等其他因素。不仅要考虑字面信息的保留，更要结合目标方言的常用表达和习惯用法来判断语义是否完整准确。不能仅从字面形式判断，需结合方言实际语境，保证语义准确对应，不能改变原句核心意思，不能仅依据是否符合方言习惯来判断，当出现可能改变原意的表达时，应优先选择与原句语义完全一致的表达。若原句语义清晰明确，原样保留原词传达信息即为符合语义完整性要求；若原句语义不完整或存在逻辑问题，在能合理推测原句意图的基础上尽量完整传达关键信息，不能简单以不添加额外信息为语义完整的标准，需根据目标方言的常用表达和习惯用法，选择能使语义更合理、更符合交流需求的表达，同时以准确表意和实际交流适用性为判断语义完整性的重要依据。原句语义不清时原样呈现也算符合要求，避免 agent 过度解读。不能因追求表达精准度、符合方言习惯等而忽略关键信息的完整保留。例如，在有关键信息替换情况时，即便表达符合方言习惯也不能判定为语义完整。"
        },
        {
            "name": "语法规范性",
            "description": "语法规范性主要聚焦于句子结构的逻辑性，但判断时需结合目标方言的表达习惯和语义理解。要以目标方言中常见的、约定俗成的语法结构和表达方式为判断标准，只要方言表达在目标方言中有合理语义和使用习惯，就应视为符合语法规范，不能仅从普通话的结构逻辑去评判，也不能仅从表面结构逻辑判断。同时，判断时要独立于其他指标，纯粹从结构上对比与原句的契合度，不能受语义、表达习惯、语义对应性等其他因素干扰。例如，在某些方言中可能存在一些与普通话不同的语序或虚词用法，只要在该方言语境中有合理语义和使用习惯，就应判定为符合语法规范。又如，给出类似原句和不同结构的方言表达，再如普通话中存在英文文本时，方言应该保持对应的英文文本，而非英文对应的解释。仅从结构上判断其逻辑性，严格按照此要求进行判断，不将其他无关因素纳入考量范围。"

        },
        {"name":"专有名词译制惯例遵循度","description": "如普通话存在专有名词，目标方言对影视 IP、角色名等专有名词若有官方译制或约定俗成的译法，需严格沿用，不存在默认为高质量数据。"},
        {"name":"数字单位方言化规范","description": "如果存在百分比、序数词等量化，表达需符合目标方言的数字使用习惯，避免生造结构或混淆单位，不存在默认为高质量数据"},
        {"name":"表达一致性","description": "方言的表达要和普通话保持一致，如果方言表达存在歧义，则表示方言文本存在问题。"},
        {"name": "英文一致性", "description": "普通话出现英文时，方言应保持英文文本一致，不能对英文进行解释"},
        {"name":"文本一致性","description": "普通话对应的方言文本不应该出现对方言文字的解释、拼音和注释等多余内容，不出现则为高质量数据,英文属于高质量"},
        {"name":"符合小爱语音助手场景","description": "方言翻译不能太口语，需要符合小爱语音助手这样得场景"},
        {"name":"连贯性","description": "方言翻译需要连贯，避免一个字一个字的翻译。"},
        {"name":"固定搭配","description": "方言中存在一些固定转换，如奥特曼对应粤语中的超人，这种属于高质量，保持原文也是高质量"}

    ],



        n_criteria=15,
        manager_prompt= "生成普通话翻译成方言的高质量评判标准",
        manager_prompt_postfix=None,
        worker_prompt=None
    )

    # 准备训练和验证数据集
    file_path = "../huayu_CritiQ/dataset/huayu_train_yue_0703.jsonl"
    with open(file_path, "r", encoding="utf-8") as f:
        train_set = [line for line in f]
    train_set = [json.loads(line) for line in train_set]
    # 调用 optimize 方法
    output_dir = "./cmx_results/0701_0.9_doubao32_yue15"
    workflow.optimize(
        train_set=train_set,
        output_dir=output_dir,
        num_epochs=5,
        threshold=(0.5, 0.9),
        save_thought=False,
        max_retries=3
    )

    print("Optimize completed. Results saved to:", output_dir)


if __name__ == "__main__":
    main()