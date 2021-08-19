import requests
import xmltodict, json
import keys
import sampledocs


class YahooAPI():
    def __init__(self):
        self.appid = keys.YAHOOAPIAPPID
        self.URL = keys.YAHOOAPIURL

    def APIprocess(self,Original_doc):
        payload = {'appid': self.appid, 'sentence': Original_doc}
        r = requests.get(self.URL, params=payload)
        return r

    def APIinfo2Fixing(self,starts,lengths,words2fix,Original_doc):
        fixeddoc = ""
        fix_rate = 0
        index = 0
        try:
            savedstart = starts[index]
            shitekilen = len(words2fix[index])
            savedlength = lengths[index]
        except:
            print("問題なし！")
            return Original_doc
        for i, s in enumerate(Original_doc):
            try:
                start,length,shitekiword = starts[index],lengths[index],words2fix[index]
            except:
                #print("once")
                start,length,shitekiword = starts[index-1],lengths[index-1],words2fix[index-1]
            #print(start,"start")
            if i  == start:
                fixeddoc += shitekiword
                fix_rate += len(shitekiword) - length
                print(fix_rate,"fix")
                shitekilen = len(shitekiword)
                savedlength = length
                savedstart = start
                index += 1
            elif savedstart <= i < savedstart + savedlength:

                print(start,"elim",start, length, fix_rate)
                pass
            else:
                fixeddoc += s

        return fixeddoc


    def Sentence_correction(self,Original_doc, APIResponse):
        #print(Original_doc)
        fix_rate = 0
        fixeddoc = ""
        starts, lengths, words2fix = [],[],[]

        #Extract Info from the APIResponse
        Parsed_response = xmltodict.parse(APIResponse.content)
        result_set = Parsed_response["ResultSet"]
        #print(result_set)
        for result_candidate in result_set:
            if type(result_set[result_candidate]) == list: #fiding the right information (Result)
                Result_important_info = result_set[result_candidate]
                print(Result_important_info)
                #print("\n")
                for i,questionable_point in enumerate(Result_important_info):
                    print(i)
                    if questionable_point["ShitekiWord"] == None:
                        continue
                    else:
                        start = int(questionable_point["StartPos"])
                        length = int(questionable_point["Length"])
                        shitekiword = questionable_point["ShitekiWord"]
                        starts.append(start)
                        lengths.append(length)
                        words2fix.append(shitekiword)

        fixeddoc = self.APIinfo2Fixing(starts,lengths,words2fix,Original_doc)
        if len(fixeddoc) == 0:
            fixeddoc = Original_doc
            print("問題なし")
        return fixeddoc

    def main(self,Original_doc):
        APIResponse = self.APIprocess(Original_doc)
        fixeddoc = self.Sentence_correction(Original_doc,APIResponse)
        print(Original_doc,"   : original doc \n")
        print(fixeddoc,"   : fixed doc")
        print(len(fixeddoc))

if __name__ == "__main__":
    doc = str(input("文書校正する日本語文書を入力,サンプル文章を使う場合は999を入力\n"))
    if doc == "999":
        doc = sampledocs.docs[0]
    yapi = YahooAPI()
    yapi.main(doc)
