# LLM Agent Architecture
參考 [Together AI](https://www.together.ai/) 的 [Explore Agent Recipes](https://www.agentrecipes.com/) Agent 範例與教學

## 常見 Agent 框架
| 類型 | 說明 |
|------|------|
| Prompt Chaining | LLM 的輸出為下一個 LLM 的輸入。這種順序設計允許結構化推理和逐步完成任務。 |
| Routing | 使用者輸入被分類到特定任務的工作流程（可以是特定的LLM 、特定提示等）。 |
| Parallelization | 使用者的提示同時傳遞給多個LLMs，一旦所有LLMs做出回應，發送到最終的LLM呼叫匯總為最終答案。 |