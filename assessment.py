from ltp import LTP

from ParaAnalysis import ParagraphAnalysis
from SentenceAnalysis import SentenceAnalysis
from Utils import cal_content_density, cal_dependency_distance, cal_corrected_TTR

ltp = LTP() # 默认加载 LTP/Small 模型


file_name = "example.txt"
file_name1 = "example1.txt"

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()  # 读取所有行

        if content:
            first_line = content[0]  # 第一行
            other_lines = ''.join(content[1:])  # 其他行合并为一个字符串
            return first_line, other_lines
        else:
            return "文件为空", ""

    except FileNotFoundError:
        return f"文件未找到: {file_path}", ""
    except Exception as e:
        return f"读取文件时出错: {e}", ""


# 读取两个文件的内容
head1,content1 = read_file(file_name)
head2,content2 = read_file(file_name1)

def analysis(para_analysis):
    cal_content_density(para_analysis)
    cal_dependency_distance(para_analysis)
    cal_corrected_TTR(para_analysis)

para_analysis = ParagraphAnalysis(content1,["cws","pos","dep"])
analysis(para_analysis)
para_analysis1 = ParagraphAnalysis(content2,["cws","pos","dep"])
analysis(para_analysis1)


def compare_metrics(dict1, dict2):
    """比较两个字典中的指标，找出相差超过10%的项"""
    diff_metrics = {}
    for key in dict1:
        if key in dict2:
            if abs(dict1[key] - dict2[key]) / max(dict1[key], dict2[key]) > 0.10:
                diff_metrics[key] = (dict1[key], dict2[key])
    return diff_metrics

different_metrics = compare_metrics(para_analysis.score, para_analysis1.score)

# 打印相差超过10%的指标
print("========================相差超过10%的指标:")
for key, values in different_metrics.items():

    print(f"Metric: {key}\n{head1}: {round(values[0],3)}\n{head2}: {round(values[1],3)}\n")

    print(f"Gap:{round((values[1]-values[0])/values[1],3)*100}%\n")
