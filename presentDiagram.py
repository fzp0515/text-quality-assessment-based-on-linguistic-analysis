import matplotlib.pyplot as plt
import numpy as np
import json

from matplotlib.font_manager import FontProperties
from sympy.physics.control.control_plots import matplotlib

with open("new_data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

llm_ls = ["gpt4", "gpt35", "glm3", "wenxin35", "deepseek"]
indicators = list(data[llm_ls[0]]["indicator"].keys())  # 假设每个LLM的指标相同，取第一个LLM的指标作为示例

# 组织数据
indicator_values = {indicator: [] for indicator in indicators}
for llm in llm_ls:
    for indicator in indicators:
        indicator_values[indicator].append(data[llm]["indicator"][indicator])


font = FontProperties(fname=r"C:\Users\Zhipeng\Desktop\MNBVC\code\linguistic\ass\新青年体.ttf")
# 绘图
fig, axs = plt.subplots(len(indicators), 1, figsize=(10, 5 * len(indicators)))
if len(indicators) == 1:  # 如果只有一个指标，确保axs是列表
    axs = [axs]


for i, indicator in enumerate(indicators):
    axs[i].bar(llm_ls, indicator_values[indicator])
    axs[i].set_title(indicator,fontproperties=font)
    axs[i].set_ylabel('Value')
    axs[i].set_xticks(range(len(llm_ls)))
    axs[i].set_xticklabels(llm_ls)

plt.show()
