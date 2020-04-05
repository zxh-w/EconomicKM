
from Model.query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict = {
            0: self.get_reigon_time_val
        }

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        return answer

    # 获取地区名字
    def get_region_name(self):
        ## 获取ns在原问题中的下标
        tag_index = self.question_flag.index("ns")
        ## 获取地区名称
        region_name = self.question_word[tag_index]
        return region_name

    def get_name(self,type_str):
        name_count=self.question_flag.count(type_str)
        if name_count==1:
            ## 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            ## 获取电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list=[]
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list


    def get_norm_x(self):
        x = re.sub(r'\D', "", "".join(self.question_word))
        return x


    # 0:n

    def get_reigon_time_val(self):
        # 获取地区名称，这个是在原问题中抽取的
        region_name=self.get_region_name()
        region_norm=self.get_name("ng")
        region_date=self.get_name("nd")
        cql = f"match (m:mydata) where m.name=~'{region_norm}.*{region_date}' return m.{region_name}"
        print(cql)
        answer = self.graph.run(cql)[0]
        print(answer)
        #answer = round(answer, 2)
        final_answer = str(region_name)+"在"+str(region_date)+"年"+str(region_norm)+"为"+str(answer)+"！"
        return final_answer
