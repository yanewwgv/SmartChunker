import time
from prompts import PROPOSITION_PROMPT
from llm_client import LLMClient
from agentic_chunker import AgenticChunker
import json
import re


def clean_json_from_model_response(response: str) -> list:
    """
    清理模型返回的 JSON 响应字符串，移除 Markdown 和多余前缀，返回 Python 对象。
    """
    # 去除 markdown 标记 ```json 或 ```，包括前后空行
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip(), flags=re.IGNORECASE)

    # 去除前缀 'json\n'（部分模型会自动加上）
    if cleaned.lower().startswith("json\n"):
        cleaned = cleaned[5:].lstrip()

    # 解析为 Python 对象
    return json.loads(cleaned)


# 初始化封装的 LLM 客户端（DashScope 兼容模式）
llm_client = LLMClient(
    api_key="sk-d2e9bfdc33ee4086aaa4b307e64ed3ee",  # 或配置环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
    pause=1.0
)

# 1. 从文件中读取原始文本并分段
with open("D:\\projects\\Agentic-Chunker\\sample_text_data.txt", "r", encoding="utf-8") as f:
    text = f.read()
paras = text.split("\n\n")


# 2. 定义提取命题的函数，调用 llm_client 的方法
def extract_propositions(paragraph: str) -> str:
    """调用封装好的 LLMClient，将段落拆分成 JSON 列表形式的命题。"""
    return llm_client.extract_propositions(paragraph, PROPOSITION_PROMPT)


# 3. 逐段生成命题并收集
all_props = []
for idx, para in enumerate(paras, start=1):
    props = extract_propositions(para)
    all_props.extend(clean_json_from_model_response(props))
    print(f"已处理第 {idx} 段，采集 {len(props)} 条命题")
    time.sleep(llm_client.pause)

print(f"总共生成命题：{len(all_props)} 条")

# 4. 演示 AgenticChunker
ac = AgenticChunker(model_name="qwen-plus")
ac.add_propositions(all_props[:5])  # 示例：只处理前5条命题
ac.pretty_print_chunks()
