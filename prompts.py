"""
此模块集中存放所有发送给 LLM 的提示（prompt）模板。
方便后续统一维护和修改。
"""

# 用于为已有 chunk 生成更新后的摘要
UPDATE_SUMMARY_PROMPT = """
你是一个 chunk 管理者。每个 chunk 里包含一组主题相关的命题。
当有新命题加入后，请根据以下内容，生成一句非常简洁的摘要，说明该 chunk 的主题，并给出后续可加入内容的指引。

Chunk 的命题列表：
{propositions}

当前摘要：
{current_summary}

只输出新的摘要，不要添加多余文字。
"""

# 用于为已有 chunk 生成更新后的标题
UPDATE_TITLE_PROMPT = """
你是一个 chunk 管理者。每个 chunk 里包含一组主题相关的命题。
当有新命题加入后，请根据以下内容，生成一个简短的标题，概括该 chunk 的主题。

Chunk 的命题列表：
{propositions}

当前摘要：
{summary}

当前标题：
{current_title}

只输出新的标题，不要添加多余文字。
"""

# 用于为新建的 chunk 生成摘要
NEW_CHUNK_SUMMARY_PROMPT = """
你是一个 chunk 管理者。请为以下单条命题生成一句非常简洁的摘要，说明该 chunk 的主题，并给出后续可加入内容的指引。

命题：
{proposition}

只输出新的摘要，不要添加多余文字。
"""

# 用于为新建的 chunk 生成标题
NEW_CHUNK_TITLE_PROMPT = """
你是一个 chunk 管理者。请为以下摘要生成一个简短的标题，概括该 chunk 的主题。

摘要：
{summary}

只输出新的标题，不要添加多余文字。
"""

# 用于在所有 chunk 中查找与新命题最匹配的 chunk
FIND_RELEVANT_PROMPT = """
给出以下所有 chunk 的 ID、标题和摘要，请判断下面的命题是否应归入已有的某个 chunk。
若应归入，请返回对应的 chunk_id；否则返回“No chunks”。

-- 当前 chunk 列表开始 --
{chunk_outline}
-- 当前 chunk 列表结束 --

待判断命题：
{proposition}
"""

# 用于将输入文本段落拆分为命题列表
PROPOSITION_PROMPT = """
请将以下段落拆解为一系列简洁明了的命题。

要求：
1. 将复合句拆分为简单句，尽量保持原句措辞。
2. 若出现带有描述性信息的实体，请将其分离为独立命题。
3. 去除上下文依赖，将所有指代（如“它”、“他”、“她”、“它们”等）替换为对应实体的全称。
4. 最终输出一个 JSON 列表，每项为字符串形式的命题。

示例：
输入：
“张三是一名医生，他在北京的协和医院工作。”
输出：
["张三是一名医生。", "张三在北京的协和医院工作。"]

请解析以下段落：
{input}
"""