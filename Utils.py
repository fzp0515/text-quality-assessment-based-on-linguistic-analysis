from math import sqrt

from SentenceAnalysis import SentenceAnalysis
from ParaAnalysis import ParagraphAnalysis
def sum_pos(freq):
    noun_tags = {'n', 'np', 'ns', 'ni', 'nz'}
    verb_tags = {'v', 'vd', 'vn'}

    sum_n = freq.get('n', 0) + freq.get('np', 0) + freq.get('ns', 0)+ freq.get('ni', 0)+ freq.get('nz', 0)
    sum_v = freq.get('v', 0) + freq.get('vd', 0) + freq.get('vn', 0)
    sum_r_c=freq.get('r', 0) + freq.get('c', 0)
    sum_other_content=freq.get('a', 0)+ freq.get('ad', 0)+ freq.get('an', 0)+ freq.get('d', 0)+ freq.get('m', 0)+ freq.get('q', 0)+ freq.get('r', 0)
    freq["sum_n"]=sum_n
    freq["sum_v"]=sum_v

    return sum_n, sum_v,sum_r_c,sum_other_content


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
    print(f"rc连贯度为{format(rc_cohesion,'.3f')}")
    analysis.score["语义密度"]=semantic_density
    analysis.score["内容密度"]=content_density
    analysis.score["rc连贯度"]=rc_cohesion

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
