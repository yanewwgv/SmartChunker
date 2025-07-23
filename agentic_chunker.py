import uuid
import time
from openai import OpenAI
from prompts import (
    UPDATE_SUMMARY_PROMPT, UPDATE_TITLE_PROMPT,
    NEW_CHUNK_SUMMARY_PROMPT, NEW_CHUNK_TITLE_PROMPT,
    FIND_RELEVANT_PROMPT
)

# 使用阿里云 DashScope 兼容模式的 OpenAI 客户端
client = OpenAI(
    api_key="sk-d2e9bfdc33ee4086aaa4b307e64ed3ee",  # 或配置环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


class AgenticChunker:
    def __init__(self, model_name="qwen-plus", pause=1.5, id_len=5):
        """
        初始化：
        - chunks: 存储所有 chunk 的字典，key 为 chunk_id
        - client: OpenAI API 客户端
        - model_name: 要使用的大模型名称
        - pause: 每次 API 调用后的等待时间，防止超限
        - id_len: 生成的 chunk_id 长度
        """
        self.chunks = {}
        self.client = client
        self.model = model_name
        self.pause = pause
        self.id_len = id_len

    def _call_llm(self, prompt: str) -> str:
        """
        通用方法：调用 chat.completions API，返回 assistant 的回复内容。
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content.strip()

    def add_propositions(self, propositions):
        """批量添加命题，每次添加后等待一段时间。"""
        for prop in propositions:
            self.add_proposition(prop)
            time.sleep(self.pause)

    def add_proposition(self, proposition):
        """向系统添加单条命题，并处理分组或新建 chunk。"""
        print(f"Adding proposition: {proposition}")
        if not self.chunks:
            print("当前无 chunk，正在创建新 chunk …")
            self.create_new_chunk(proposition)
            return

        cid = self.find_relevant_chunk(proposition)
        if cid:
            print(f"找到匹配 chunk ({cid})，正在合并 …")
            self._append_to_chunk(cid, proposition)
        else:
            print("未找到匹配 chunk，正在创建新 chunk …")
            self.create_new_chunk(proposition)

    def _append_to_chunk(self, chunk_id, proposition):
        """将命题加入已有 chunk，并更新摘要与标题。"""
        chunk = self.chunks[chunk_id]
        chunk["propositions"].append(proposition)

        # 更新摘要
        summary_prompt = UPDATE_SUMMARY_PROMPT.format(
            propositions=chunk["propositions"],
            current_summary=chunk["summary"]
        )
        chunk["summary"] = self._call_llm(summary_prompt)

        # 更新标题
        title_prompt = UPDATE_TITLE_PROMPT.format(
            propositions=chunk["propositions"],
            summary=chunk["summary"],
            current_title=chunk["title"]
        )
        chunk["title"] = self._call_llm(title_prompt)

    def create_new_chunk(self, proposition):
        """创建一个新的 chunk，包含初始命题、摘要、标题及索引。"""
        new_id = str(uuid.uuid4())[:self.id_len]
        # 调用 LLM 生成摘要
        summary_prompt = NEW_CHUNK_SUMMARY_PROMPT.format(proposition=proposition)
        summary = self._call_llm(summary_prompt)
        # 调用 LLM 生成标题
        title_prompt = NEW_CHUNK_TITLE_PROMPT.format(summary=summary)
        title = self._call_llm(title_prompt)

        self.chunks[new_id] = {
            "chunk_id": new_id,
            "propositions": [proposition],
            "title": title,
            "summary": summary,
            "index": len(self.chunks)
        }
        print(f"创建新 chunk ({new_id})：{title}")

    def find_relevant_chunk(self, proposition):
        """判断命题是否应归入某个已有 chunk，返回匹配的 chunk_id 或 None。"""
        outline = "\n".join(
            f"Chunk ID: {c['chunk_id']}\nTitle: {c['title']}\nSummary: {c['summary']}\n"
            for c in self.chunks.values()
        )
        find_prompt = FIND_RELEVANT_PROMPT.format(
            chunk_outline=outline,
            proposition=proposition
        )
        resp = self._call_llm(find_prompt)
        return resp if len(resp) == self.id_len else None

    def pretty_print_chunks(self):
        """格式化输出当前所有 chunk 的内容。"""
        print("\n----- 当前 Chunks -----\n")
        for c in self.chunks.values():
            print(f"ID      : {c['chunk_id']}")
            print(f"标题    : {c['title']}")
            print(f"摘要    : {c['summary']}")
            print("命题列表:")
            for p in c["propositions"]:
                print(f"  - {p}")
            print()
