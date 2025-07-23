from openai import OpenAI
import time


class LLMClient:
    """
    封装 OpenAI 客户端与调用逻辑。
    - 配置 DashScope 兼容模式
    - 提供统一的 LLM 接口方法
    - 支持提取命题的专用方法
    """
    def __init__(self, api_key: str, base_url: str, model: str = "qwen-plus", pause: float = 1.0):
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.pause = pause

    def call(self, prompt: str) -> str:
        """通用调用 LLM，返回文本结果。"""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        # 调用后等待，可以根据需要调整
        time.sleep(self.pause)
        return resp.choices[0].message.content.strip()

    def extract_propositions(self, paragraph: str, prompt_template: str) -> str:
        """
        将段落拆解成命题列表。
        - prompt_template: 包含 {input} 的字符串模板
        """
        result = self.call(prompt_template.format(input=paragraph))
        return result
