import pandas as pd

#phrase pattern function
def pattern_writer(key_ans): #typo
    df = pd.read_excel("phrase_patterns.xlsx")
    dict_ = {key_ans[0] : key_ans[1]}
    df1 = pd.DataFrame.from_dict(dict_)
    if key_ans[0] in list(df.columns):
        df = df.append(df1)
    else:
        df = pd.concat([df, df1], axis = 1)
    df = df.fillna('')
    df.to_excel("phrase_patterns.xlsx", index=False, encoding='utf8')
    return None
    
def pattern_reader():
    df = pd.read_excel("phrase_patterns.xlsx")
    df = df.fillna('')
    dict_ = df.to_dict('list')
    return dict_
    
keywords_phrase_list = pattern_reader()

# keywords_phrase_list = {
#     "beyond meat".lower() : ["beyond meat"],
#     "gene editing".lower() : ["gene editing", "gene edit"],
#     ......
#     }
