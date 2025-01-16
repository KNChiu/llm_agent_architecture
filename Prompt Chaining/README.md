# Prompt Chaining 範例
LLM 的輸出為下一個 LLM 的輸入。這種順序設計允許結構化推理和逐步完成任務。
使用 OpenAI 的大型語言模型 (LLM) 進行提示鏈 (Prompt Chaining)。

`serial_chain_workflow` 函數接收一個初始問題 (`input_query`) 和一個提示列表 (`prompt_chain`)。 
它會依序將問題傳遞給 LLM，並使用 `prompt_chain` 中的每個提示來逐步處理問題。

腳本會列印出每個步驟的輸出結果，最終答案會儲存在 final_answer 變數中。

## 輸出結果
```bash
Step 1
Sally earns $12 an hour for babysitting and did 50 minutes of babysitting yesterday.

Step 2
1. Convert 50 minutes to hours by dividing by 60: 50 minutes / 60 = 0.83 hours.
2. Calculate the earnings by multiplying the hourly rate by the number of hours worked: $12/hour x 0.83 hours = $9.96.

Step 3
The final answer is $9.96.
```