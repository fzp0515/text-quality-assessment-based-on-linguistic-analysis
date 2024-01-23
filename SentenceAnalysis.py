from collections import Counter
from ltp import LTP
from ltp import StnSplit
class SentenceAnalysis:
    def __init__(self, text,task):
        self.text = text
        self.task=task
        self.length=len(self.text)
        self.result_dic=self._analysis()
        self.pos_freq=Counter(self.result_dic["pos"])

    def _analysis(self):
        ltp = LTP()
        result_dic={}
        result = ltp.pipeline([self.text], tasks=self.task)
        if "cws" in self.task:
            result_dic["cws"]=result.cws[0]
        if "pos" in self.task:
            result_dic["pos"]=result.pos[0]
        if "dep" in self.task:
            result_dic["dep"]=result.dep[0]
        if "sdp" in self.task:
            result_dic["sdp"]=result.sdp[0]
        if "sdpg" in self.task:
            result_dic["sdpg"]=result.sdpg[0]
        return result_dic


    def __str__(self):
        for key, value in self.result_dic.items():
            print(f"{key}: {value}")
        return (f"Text: {self.text}\n")

