# Character-Chat: 虚拟角色复活计划

> 让 AI 扮演你喜爱的虚拟角色，满足自己的一切愿望！

**项目简介**

受到 Deepseek 和 ChatGPT 的启发，本项目旨在利用大语言模型（LLM）强大的上下文理解能力，让 AI 扮演虚拟角色，实现与角色的深度互动。通过精心设计的知识库、Prompt 工程和低成本的 API 方案，你可以在 Telegram 上与“复活”的虚拟角色进行自然、流畅的对话。

**项目灵感**

最近 Deepseek 的火爆让我重燃了当初 ChatGPT 刚问世时的想法：让 AI 扮演虚拟角色，不仅可以辅助游戏，更能满足与角色互动的心愿。经过一段时间的研究，我摸索出了一套低成本、可行的方案（虽然最终因 Deepseek 的上下文长度限制而未使用）。

**核心优势**

*   **深度沉浸**：通过海量知识库和精细 Prompt，让 AI 深刻理解角色背景、性格和故事。
*   **自然交互**：利用先进的 LLM 和 Rerank 模型，实现流畅、自然的对话体验。
*   **低成本**：充分利用免费或低成本的 API 资源，降低使用门槛。
*   **易于部署**：基于 Docker 和 Dify，提供详细的部署指南，方便快速搭建。
*   **灵活扩展**：支持自定义知识库、Prompt 和模型，满足个性化需求。

**快速开始**

### 一、准备工作

1.  **大上下文模型 API Key**：
    *   推荐使用免费的 Google Gemini，其 Flash 模型提供 100k 上下文 token。
    *   申请地址：[https://aistudio.google.com](https://aistudio.google.com) （需 Google 账号）。

2.  **文档嵌入、Rerank 和语音模型 API Key**：
    *   可选方案：
        *   **Ollama**：本地搭建，提供更强的控制力和隐私性。
        *   **硅基流动**：目前提供免费 API，方便快捷。注册地址：[https://siliconflow.cn/zh-cn/](https://siliconflow.cn/zh-cn/)。
    * 语音转文字为可选

3.  **Dify 运行环境**：
    *   **服务器或电脑**：满足以下最低配置：
        *   CPU >= 2 Core
        *   RAM >= 4 GiB
    *   **推荐**：Windows Docker（本文档提供详细教程）。

### 二、安装与配置 Dify

1.  **Docker 安装**：
    *   参考官方文档：[https://docs.dify.ai/zh-hans/getting-started/install-self-hosted/docker-compose](https://docs.dify.ai/zh-hans/getting-started/install-self-hosted/docker-compose)

2.  **固定局域网 IP**：
    *   在路由器中为你的电脑设置静态 IP，用于后续 Telegram Bot 通信。

3.  **Dify 环境变量调整**：
    *   修改 Dify 容器的 `.env` 文件：
        *   `TOP_K_MAX_VALUE`：知识库召回片段上限，建议 `1000`。
        *   `INDEXING_MAX_SEGMENTATION_TOKENS_LENGTH`：分段最大 token 数，建议 `1048000`。

4.  **访问 Dify**：
    *   浏览器输入 `http://你的局域网IP`。

5.  **Dify 配置**：
    *   模型选择：根据当前最佳模型自行选择。
    *   详细配置参考 Dify 官方文档。

### 三、构建角色知识库

1.  **知识来源**：
    *   游戏对话文本（如 Ren'Py 提取的对话）。
    *   角色背景设定、故事梗概、同人创作等。

2.  **文本处理**：
    *   使用项目提供的 `trans.py` 脚本处理 Ren'Py 提取的 `.tab` 文件。
    *   将 `.tab` 文件拖拽到 `trans.py` 上即可生成格式化文本。
    *   **示例格式**：
        ```
        driverCheck-boa: 我们还缺了谁？所有人明明都到了              前缀-角色:具体文本
        ```

3.  **知识库设置**：
    *   **分段策略**：父子分段。
        *   父段落：5000 token。
        *   子段落：2000 token。
    *   **检索方式**：混合检索 + Rerank 模型。
    *   **Top K**：20-100（根据实际效果调整）。

### 四、创建 Dify 应用

1.  **应用类型**：空白应用 -> 聊天助手模板。
2.  **功能开启**：根据需要开启视觉功能等。
3.  **Prompt 工程**：
    *   使用 Gemini 1.5 Pro（200k 上下文）等模型分析完整文本，提炼角色性格、说话方式等信息。
    *   参考示例：

    > 我希望你能分析、理解并记住发生的事情和人物的性格，然后尽量精简的归纳总结发生的事情和人物的性格。
    >
    > 现在请你总结聊天机器人扮演 Orlando 需要注意的地方，特别是关于 orlando 的性格、情感、伤痛和说话方式，还有就是与他本人相关的令人难忘的情节。
    >
    > 请详细总结 Orlando 的说话方式。
    * 丰富prompt
    * 可以参考`参考`文件夹

4.  **知识库说明**：
    *   在 Prompt 中向 AI 解释知识库文本的格式和含义。
    *   示例：
        ```
        后续会给你一大段视觉小说提取出来的文本以及一些剧情的归纳和总结，他是根据别人的提问从知识库抽出的，所以不一定完整，有不同的角色说的话和背景描写，这个故事是一个有多条线路不同时间点的复杂故事，给你的文本结构是前缀-角色:具体文本，前缀就是表示出现的场景或者线路，比如driver_Wilson就是选了Wilson当司机的线路发生的事情，然后day1就是第一天发生的事情，Day13AB就是AB线路共通剧情，总共有ABCDFGP七条线路，A_R这个标识表示的就是P线路，我没有详细解释的前缀你可以根据词义自己理解一下，然后-后面跟随的含义是，bac就是背景描写，ext是上一段描写或者对话的延续，dra是Orlando，bea是Dean，boa是Roswell，wol是Tyson，lio是Hoss，cro是Sal，mc或者dav就是Dave，其他的你可以自己分析判断一下。
        ```

### 五、配置 Telegram Bot

1.  **创建 Bot**：
    *   参考 Telegram Bot 创建教程。

2.  **连接 Dify 与 Telegram**：
    *   在 Dify 应用中创建 API 密钥。
    *   使用 [https://github.com/CyanidEEEEE/dify-telegram_bot](https://github.com/CyanidEEEEE/dify-telegram_bot) 项目连接。

**开始对话！**

现在，你可以在 Telegram 上与你的虚拟角色聊天了！

**贡献**

欢迎提交 Issue 和 Pull Request，一起完善本项目！
