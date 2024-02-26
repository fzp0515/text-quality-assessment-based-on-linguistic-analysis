from ltp import LTP

from ParaAnalysis import ParagraphAnalysis
from SentenceAnalysis import SentenceAnalysis
from Utils import cal_content_density, cal_dependency_distance, cal_corrected_TTR, cal_parse_tree_height, \
    cal_lexical_cohesion, cal_constituent, cal_proportion_char_length
import json

ltp = LTP()  # 默认加载 LTP/Small 模型
llm_ls = ["gpt4", "gpt35", "glm3", "wenxin35", "deepseek"]
# file_name = "example.txt"
# file_name1 = "example1.json"


# def read_file(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.readlines()  # 读取所有行
#
#         if content:
#             first_line = content[0]  # 第一行
#             other_lines = ''.join(content[1:])  # 其他行合并为一个字符串
#             return first_line, other_lines
#         else:
#             return "文件为空", ""
#
#     except FileNotFoundError:
#         return f"文件未找到: {file_path}", ""
#     except Exception as e:
#         return f"读取文件时出错: {e}", ""


# test_text="它通常表现为拒绝承认负面事件或将其归因于外部因素，以减少个体的心理负担。例如，当面临亲人去世等重大打击时，人们可能会下意识地否认事实，认为这不是真的。虽然这种机制在某些情况下有助于减轻痛苦，但过度使用可能导致个体忽视现实问题，甚至导致心理障碍。"
# sent=SentenceAnalysis(test_text,["cws","pos","dep","sdpg"])
# print(sent)

# 读取两个文件的内容
# head1, content1 = read_file(file_name)


def analysis(para_analysis):
    cal_content_density(para_analysis)
    cal_dependency_distance(para_analysis)
    cal_corrected_TTR(para_analysis)
    cal_constituent(para_analysis)
    cal_parse_tree_height(para_analysis)
    cal_lexical_cohesion(para_analysis)
    cal_proportion_char_length(para_analysis)


def read_json(file):
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for llm in llm_ls:
            print(f"开始对{llm}的回答进行语言学分析")
            llm_answer_analysis = ParagraphAnalysis(data[llm]["answer"], ["cws", "pos", "dep","sdpg"])
            analysis(llm_answer_analysis)
            data[llm]["indicator"]=llm_answer_analysis.score



    with open('new_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



read_json("test.json")





















# def get_eval(llm):
#     result = {"answer": "",
#               "indicator": {},
#               "scoreFromGpt35": "",
#               "explainFromGpt35": {}}
#
#     if result
#
#
#
#     return result
#
#
# def fill_in_json(prompt):
#
#     data = {
#         "prompt": prompt,
#     }
#
#     for name in llm_ls:
#         eval_result = get_eval(name)
#         data[name] = eval_result
#
#     with open('data.json', 'w') as file:
#         json.dump(data, file, indent=4)




# def compare_metrics(dict1, dict2):
#     """比较两个字典中的指标，找出相差超过10%的项"""
#     diff_metrics = {}
#     for key in dict1:
#         if key in dict2:
#             if abs(dict1[key] - dict2[key]) / max(dict1[key], dict2[key]) > 0.10:
#                 diff_metrics[key] = (dict1[key], dict2[key])
#     return diff_metrics
#
# different_metrics = compare_metrics(para_analysis.score, para_analysis1.score)
#
# # 打印相差超过10%的指标
# print("========================相差超过10%的指标:")
# for key, values in different_metrics.items():
#
#     print(f"Metric: {key}\n{head1}: {round(values[0],3)}\n{head2}: {round(values[1],3)}\n")
#
#     print(f"Gap:{round((values[1]-values[0])/values[1],3)*100}%\n")
