# Smart Chunker 项目

# 项目概述

Smart Chunker 是一个基于大模型（LLM）的文本分块（chunking）工具，能够将长文本拆分为一系列命题（propositions），并将这些命题按照主题相似性动态组织到多个chunks 中，形成高效的文本分块方案，便于后续的检索、摘要生成和知识管理。

## 主要功能：
命题抽取：将输入文本拆分为简明、独立的命题。

动态分块：根据命题之间的关联，将相似命题自动归入同一 chunk，不同则创建新的 chunk。

摘要与标题生成：为每个 chunk 自动生成概括性的摘要和标题，便于快速浏览和理解。

## 适用场景：
RAG（Retrieval-Augmented Generation）系统中的文本预处理

知识图谱构建中的事实抽取与主题归类

文本分析与信息检索中的结构化分块


# 安装与依赖

## 克隆仓库
git clone https://github.com/yanewwgv/SmartChunker.git
cd SmartChunker

## 安装依赖（需事先 pip 已配置）
pip install -r requirements.txt

主要依赖：

    -openai：用于调用大模型 API（支持 Aliyun DashScope 兼容模式）

    -uuid、time：核心 Python 库

    （可根据需要添加）

## 配置说明
API Key 与 Base URL在 llm_client.py 中，或通过环境变量配置 Aliyun DashScope 兼容模式：

    client = OpenAI(
        api_key="sk-xxx",  # 替换为实际 API Key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

模型名称默认使用 qwen-plus，可根据实际需求更换为其他支持的中文大模型。

Prompt 模板所有与模型交互的 Prompt 都集中在 prompts.py，可自行修改或扩展。



# 贡献指南

欢迎提交 Issue 与 Pull Request。请遵循以下流程：

1. Fork 本仓库。

2. 新建分支：git checkout -b feature/your-feature。

3. 提交代码并推送：git push origin feature/your-feature。

4. 创建 Pull Request，描述功能及实现细节。

# 授权协议

本项目采用 MIT 协议，详见 LICENSE。