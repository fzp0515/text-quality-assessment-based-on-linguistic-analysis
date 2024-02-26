from math import sqrt
import numpy as np
from SentenceAnalysis import SentenceAnalysis
from ParaAnalysis import ParagraphAnalysis
noun_tags = {'n', 'np', 'ns', 'ni', 'nz'}
verb_tags = {'v', 'vd', 'vn'}
adj_tags={'a','ad','an'}
def sum_pos(freq):


    sum_n = freq.get('n', 0) + freq.get('np', 0) + freq.get('ns', 0)+ freq.get('ni', 0)+ freq.get('nz', 0)
    sum_v = freq.get('v', 0) + freq.get('vd', 0) + freq.get('vn', 0)
    sum_r_c=freq.get('r', 0) + freq.get('c', 0)
    sum_other_content=freq.get('a', 0)+ freq.get('ad', 0)+ freq.get('an', 0)+ freq.get('d', 0)+ freq.get('m', 0)+ freq.get('q', 0)+ freq.get('r', 0)
    freq["sum_n"]=sum_n
    freq["sum_v"]=sum_v

    return sum_n, sum_v,sum_r_c,sum_other_content


def cal_constituent(para:ParagraphAnalysis):
    # 初始化统计字典
    phrase_counts = {'NP': 0, 'VP': 0, 'PP': 0, 'CP': 0, 'Adj': 0}
    for sent in para.sentences:
        for i, (pos_tag, label) in enumerate(zip(sent.result_dic["pos"], sent.result_dic["dep"]["label"])):
            if label == 'ATT' and pos_tag in noun_tags:  # 名词短语
                phrase_counts['NP'] += 1
            elif label in ['VOB', 'CMP'] and pos_tag in verb_tags:  # 动词短语
                phrase_counts['VP'] += 1
            elif label == 'POB' and pos_tag == 'p':  # 介词短语
                phrase_counts['PP'] += 1
            elif label == 'COO':  # 并列短语
                phrase_counts['CP'] += 1
            elif label == 'ATT' and pos_tag in adj_tags:  # 形容词修饰语
                phrase_counts['Adj'] += 1
    new_dict = {key: value*100 / para.length for key, value in phrase_counts.items()}

    print(new_dict)
    para.score["count_constituent"]=0
    for key in new_dict:
        para.score[key] = new_dict[key]
        para.score["count_constituent"]+=new_dict[key]
    print(para.score["count_constituent"])




def cal_content_density(analysis:ParagraphAnalysis):
    n_sum=0
    v_sum=0
    rc_sum=0
    othercontent_sum=0
    for sent in analysis.sentences:
        n,v,rc,other_content=sum_pos(sent.pos_freq)
        n_sum+=n
        v_sum+=v
        rc_sum+=rc
        other_content+=othercontent_sum
    semantic_density, content_density,rc_cohesion=n_sum/ analysis.length,(n_sum + v_sum+othercontent_sum) / analysis.length,rc_sum/analysis.length
    print(f"语义密度为{format(semantic_density,'.3f')}")
    print(f"内容密度为{format(content_density,'.3f')}")
    print(f"代连词连贯度为{format(rc_cohesion,'.3f')}")
    analysis.score["语义密度"]=semantic_density
    analysis.score["内容密度"]=content_density
    analysis.score["代连词连贯度"]=rc_cohesion

def cal_dependency_distance(para:ParagraphAnalysis):
    max_root_dist,avr_root_dist,max_depend_dist,avr_depend_dist=0,0,0,0

    for sent in para.sentences:
        ls=sent.result_dic["dep"]["head"]
        max_depend_dist=max(max_depend_dist,max(ls))
        max_root_dist=max(max_root_dist,ls.index(0) if 0 in ls else len(ls)/2)
        avr_root_dist+=ls.index(0) if 0 in ls else len(ls)/2
        avr_depend_dist+=sum(ls)/len(ls)
    avr_root_dist/=para.sent_count
    avr_depend_dist/=para.sent_count
    print(f"max root distance:{max_root_dist}")
    print(f"avr root distance:{avr_root_dist}")
    print(f"max depend distance:{max_depend_dist}")
    print(f"avr depend distance:{avr_depend_dist}")
    para.score["max root dist"]=max_root_dist
    para.score["avr root dist"]=avr_root_dist
    para.score["max depend dist"]=max_depend_dist
    para.score["avr depend dist"]=avr_depend_dist
    # return max_root_dist,avr_root_dist,max_depend_dist,avr_depend_dist


def cal_corrected_TTR(para:ParagraphAnalysis):
    unique_set={0}
    token_count=0

    for sent in para.sentences:
        ls=list(sent.result_dic["cws"])
        unique_set.update(ls)
        token_count+=len(sent.result_dic["cws"])

    CTTR=len(unique_set)/sqrt(2*token_count)
    print(f"CTTR:{format(CTTR,'.3f')}")
    para.score["CTTR"]=CTTR

    # return CTTR

def cal_parse_tree_height(para:ParagraphAnalysis):
    trees_depth=[]
    for sent in para.sentences:
        heads=sent.result_dic["dep"]["head"]
        children = build_tree(heads)
        depth = tree_depth(heads.index(0), children)
        trees_depth.append(depth)
        # print(f"解析树的深度为: {depth}")

    average = np.mean(trees_depth)
    std_dev = np.std(trees_depth)
    max_value = max(trees_depth)
    # 计算超过14的个数
    proportion_over_14 = sum(1 for num in trees_depth if num > 14)/len(trees_depth)
    print(f"avr tree depth:{average}")
    print(f"max tree depth:{max_value}")
    print(f"std_dev of tree depth:{std_dev}")
    print(f"tree depth count_over_14:{proportion_over_14}")
    para.score["avr tree depth"] = average
    para.score["max tree depth"] = max_value
    para.score["std_dev of tree depth"] = std_dev
    para.score["tree depth proportion_over_14"] = proportion_over_14


    # 构建树结构
def build_tree(heads):
    children = [[] for _ in heads]
    for child_index, parent_index in enumerate(heads):
        if parent_index != 0:  # 0表示根节点
            children[parent_index - 1].append(child_index)
    return children

# 递归计算树的深度
def tree_depth(node, children):
    if not children[node]:  # 如果没有子节点
        return 1
    else:
        # 深度是所有子节点的深度中的最大值加1
        return 1 + max(tree_depth(child, children) for child in children[node])


def extract_pos_words(words, pos_tags, target_pos_tags):
    """从句子中提取特定词性的词"""
    return [word for word, pos_tag in zip(words, pos_tags) if pos_tag in target_pos_tags]

def calculate_similarity(words1, pos1, words2, pos2, target_pos_tags):
    """计算两个句子中相同词的占比"""
    words_set1 = set(extract_pos_words(words1, pos1, target_pos_tags))
    words_set2 = set(extract_pos_words(words2, pos2, target_pos_tags))
    common_words = words_set1.intersection(words_set2)
    total_words = len(words_set1) + len(words_set2)
    return len(common_words) / total_words if total_words > 0 else 0



def cal_lexical_cohesion(para:ParagraphAnalysis):
    """分析文本中句子lexical cohesion"""
    target_pos_tags = ['n', 'np', 'ns', 'ni', 'v', 'vd', 'vn', 'a', 'ad', 'an', 'd']
    adjacent_similarity = []
    non_adjacent_similarity = []
    sentences=[]
    for sent in para.sentences:
        sentences.append((sent.result_dic["cws"],sent.result_dic["pos"]))

    for i in range(len(sentences)):
        current_words, current_pos = sentences[i]
        # 前一句
        if i > 0:
            prev_words, prev_pos = sentences[i - 1]
            adjacent_similarity.append(calculate_similarity(current_words, current_pos, prev_words, prev_pos, target_pos_tags))
        # 后一句和后二句
        if i < len(sentences) - 2:
            for j in range(i + 1, min(i + 3, len(sentences))):
                next_words, next_pos = sentences[j]
                adjacent_similarity.append(calculate_similarity(current_words, current_pos, next_words, next_pos, target_pos_tags))

    # 分析非邻近句子（排除当前句子及其相邻句子）
    for i in range(len(sentences)):
        current_words, current_pos = sentences[i]
        for j in range(len(sentences)):
            if j < i - 1 or j > i + 2:  # 排除当前句子及其相邻句子
                words1, pos1 = sentences[j]
                non_adjacent_similarity.append(calculate_similarity(current_words, current_pos, words1, pos1, target_pos_tags))

    adjacent_cohesion=sum(adjacent_similarity) / len(adjacent_similarity) if len(adjacent_similarity) else 0
    non_adjacent_cohesion=sum(non_adjacent_similarity) / len(non_adjacent_similarity) if len(non_adjacent_similarity) else 0
    print(adjacent_cohesion)
    print(non_adjacent_cohesion)


def cal_proportion_char_length(para:ParagraphAnalysis):
    phrase_counts = {'one_char': 0, 'two_char': 0, 'three_char': 0, 'four_char': 0}
    for sent in para.sentences:
        for word in sent.result_dic["cws"]:
            length = len(word)
            if length == 1:
                phrase_counts["one_char"] += 1
            elif length == 2:
                phrase_counts["two_char"] += 1
            elif length == 3:
                phrase_counts["three_char"] += 1
            elif length >= 4:
                phrase_counts["four_char"] += 1
    new_dict = {key: value/ para.length for key, value in phrase_counts.items()}

    print(new_dict)
    for key in new_dict:
        para.score[key] = new_dict[key]


