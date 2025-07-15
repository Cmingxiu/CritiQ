import json
import os
from argparse import ArgumentParser
from pathlib import Path

from CritiQ.my_CritiQ.critiq.workflow_mify import Workflow
from CritiQ.my_CritiQ.critiq.evaluator_mify import PairEvaluator, ZeroOneEvaluator
from openai import OpenAI  # 使用标准 OpenAI 客户端

# deepseek
deepseek_APP_KEYS = [
     "Bearer app-FlExJjoQFNLtxxxxxxxxxxxx",
]

# 豆包
doubao_APP_KEYS = [ 
]

# qwen 3
qwen_APP_KEYS =[
    "Bearer app-FlExJjoQFNLt",
    
]



def main(args):
    print(args)

    file_name = args.data.split("/")[-1].split(".")[0]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_file_path = Path(args.output_dir) / f"{file_name}.jsonl"

    with open(args.data, "r", encoding="utf8") as f:
        dataset = [line for line in f]

    start_from = 0
    if save_file_path.exists():
        with open(save_file_path, "r", encoding="utf8") as f:
            for _ in f:
                start_from += 1

    dataset = [json.loads(line) for line in dataset[start_from:]]


    client = OpenAI(
        api_key=args.api_key,
        base_url=args.base_url,
    )

    WORKER_ARGS = {
        "api_keys": args.api_key,
        "base_url":args.base_url,
    }

    workflow = Workflow()
    workflow.load(args.workflow)

    if "A" in dataset[0] and "B" in dataset[0]:
        evaluator_class = PairEvaluator
        output_field = "answer"
    elif "text" in dataset[0]:
        evaluator_class = ZeroOneEvaluator
        output_field = "label"
    else:
        raise ValueError("Unknown dataset format")

    idx = 0
    if args.worker_prompt_postfix_file:
        with open(args.worker_prompt_postfix_file, "r", encoding="utf8") as f:
            evaluator_class.worker_prompt_postfix = f.read()

    while idx < len(dataset):

        print(f"Processing [{start_from+idx}, {start_from+idx+MAX_CONCURRENT})")
        evaluator = evaluator_class(
            WORKER_ARGS,
            dataset=dataset[idx : idx + MAX_CONCURRENT],
            max_concurrent=MAX_CONCURRENT,
            max_retries=3,
            worker_prompt=args.worker_prompt or workflow.worker_prompt,
            max_data_chars=args.max_data_chars,
        )
        pred_output = evaluator.pred(
            workflow.get_best_criteria(args.criterion_threshold),
            threshold=args.voting_threshold,
        )

        for i in range(len(pred_output.prediction)):
            simplified_scores = {}
            for criterion in pred_output.prediction[i].keys():                                                                                                                                                                                                  
                scores = pred_output.prediction[i][criterion]
                if scores[0] == scores[1]:
                    simplified_scores[criterion] = "none"
                else:
                    best_key = max(scores.items(), key=lambda x: x[1])[0]
                    simplified_scores[criterion] = best_key

            pred_output.prediction[i] = simplified_scores
        
        
        with open(save_file_path, "a", encoding="utf8") as f:
            for d, p, t, s in zip(
                dataset[idx : idx + MAX_CONCURRENT],
                pred_output.answer,
                pred_output.thoughts,
                pred_output.prediction
            ):
                f.write(
                    json.dumps(
                        {**d, output_field: p, "all_label": s,"thought": t}, ensure_ascii=False
                    )
                    + "\n"
                )

        idx += MAX_CONCURRENT


def cli():
    parser = ArgumentParser()
    parser.add_argument("--api_key", type=list, default=qwen_APP_KEYS)
    parser.add_argument("--base_url", type=str, default="https://mify-be.pt.xiaomi.com/api/v1/workflows/run")
    parser.add_argument("--workflow", type=str, default="./cmx_results/mify_qwen3_yue15/epoch_final.json")
    parser.add_argument("--data", type=str, default="./dataset/soundbox_yue.jsonl")
    parser.add_argument("--worker_prompt", type=str, required=False)
    parser.add_argument("--worker_prompt_postfix_file", type=str, required=False)
    parser.add_argument("--output_dir", type=str, default="./cmx_results/annot_qwen3_15")
    parser.add_argument("--criterion_threshold", type=float, default=0.9)
    parser.add_argument("--voting_threshold", type=float, default=0.9)
    parser.add_argument("--max_data_chars", type=int)
    main(parser.parse_args())

# 控制最大并发数
MAX_CONCURRENT = int(os.getenv("WORKER_MAX_CONCURRENT", "100"))


if __name__ == "__main__":
    cli()