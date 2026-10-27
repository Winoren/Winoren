<div align="center">

# 董思俊 · Winoren

**AI Agent Developer · Backend Engineering**

关注 Agent Runtime、MCP、上下文工程与可评测的业务工作流

[GitHub](https://github.com/Winoren) · [开源贡献](CONTRIBUTIONS.md) · [邮件联系](mailto:d2572973337@qq.com)

</div>

---

### ABOUT ME

软件工程本科在读，关注如何让 AI Agent 在真实业务中可靠地使用数据和工具。

我的兴趣覆盖 **Tool Calling、Agent Harness、RAG、长期记忆、权限控制与 Eval**。我喜欢从具体业务问题出发，思考如何让 Agent 的行为可追踪、可验证，并在关键节点由人做决定。

- 🎓 湖北第二师范学院 · 软件工程 · 2027 届
- 🏢 实习经历：中国电信、美的集团
- 🏆 第十五届蓝桥杯软件赛全国一等奖、睿抗编程技能竞赛全国二等奖
- 🌱 持续参与 Agent、LLM 与 RAG 相关开源项目

---

### OPEN SOURCE

**59 个 PR 已合并 · 20 个开源仓库**

参与 Agent 框架与 LLM 应用生态的缺陷修复，关注工具调用、流式响应、知识检索、数据处理与运行可靠性。

| 项目 | 贡献 |
| :--- | :--- |
| [langroid/langroid](https://github.com/langroid/langroid) | 21 个 PR 已合并 |
| [langgenius/dify](https://github.com/langgenius/dify) | 10 个 PR 已合并 |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 5 个 PR 已合并 |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 3 个 PR 已合并 |
| [NVIDIA/NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | 1 个 PR 已合并 |
| [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | 1 个 PR 已合并 |

**一些具体工作**

- **Dify**：修复 Node.js SDK 中 SSE 字段空白处理、请求头大小写合并等问题，也参与知识段索引状态与服务端事务边界问题的修复。
- **deer-flow**：修复 Skills 元数据解析和搜索结果处理中的边界问题。
- **Langroid**：修复 Agent 异步执行、文档切分、Embedding 配置和工具结果处理等问题。

[查看贡献明细 →](CONTRIBUTIONS.md) · [查看 GitHub 已合并 PR →](https://github.com/pulls?q=is%3Apr+author%3AWinoren+is%3Amerged)

<sub>统计为 2026 年 10 月的快照，后续可按 GitHub 记录更新。</sub>

---

### EXPERIENCE

**美的集团 · 实习**　`2026.03 — 2026.10`

围绕制造质量管理场景，探索将 Agent 接入检验数据和不合格品处置流程。

- 将检验标准、报检单和供应商主数据封装为只读 MCP 工具，供 Agent 查询。
- 在工具执行前设置权限拦截和人工确认，针对重大质量决策衔接审批流程。
- 按报检单装配检验标准、历史案例等上下文，支持检验研判与 NCR 处置建议。

**中国电信 · 实习**

CMP 相关项目经历。

---

### SELECTED PROJECTS

#### QMS · 质量管理与智能辅助

面向质量检验和不合格品处置场景的业务系统与 Agent 实践。

- **MCP 数据接入**：以适配器封装多类质量数据，供 Agent 按业务场景查询。
- **上下文装配**：聚合报检单、标准条款和历史 NCR 案例，按 token 预算组织输入。
- **受控处置流程**：串联缺陷查询、相似案例检索和处置草稿生成，提交环节保留人工决策。

`MCP` `Tool Calling` `Context Engineering` `Human-in-the-loop`

#### AI Native CRM · 客户经营 Agent 平台

面向客户会话、商机和知识库的 Agent 工作台，将业务数据、工具调用与执行过程连接起来。

- **CRM 工具与权限**：通过 MCP、Schema 和角色范围约束工具调用，区分查询、更新和客户外发等操作。
- **知识与记忆**：结合 CRM 确认事实、知识检索和记忆服务，为客户调查提供上下文。
- **执行与评测**：关注任务恢复、幂等、工具观察、语义评测与业务结果核验。

`TypeScript` `Next.js` `MCP` `Supabase` `Mem0` `Langfuse`

---

### TECH STACK

| 领域 | 技术与关注点 |
| :--- | :--- |
| **AI Agent** | Agent Runtime、Harness、Tool Calling、MCP、多 Agent 协作 |
| **知识与记忆** | RAG、上下文工程、记忆分层、向量检索 |
| **可靠性** | 权限控制、人工审批、事件追踪、幂等与故障恢复 |
| **评测与观测** | Agent Eval、语义评测、Langfuse、回归验证 |
| **语言与工程** | TypeScript、Python、JavaScript、Java、SQL、Git、Docker、Linux |

---

<div align="center">

**把模型能力连接到真实业务，让每一次行动都有依据。**

</div>
