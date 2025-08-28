import re
import json

abbreviations = {
    "_Fran._": "Francisco",
    "_Hor._": "Horatio",
    "_Mar._": "Marcellus",
    "_Ber._": "Bernardo",
    "_King._": "King",
    "_Queen._": "Queen",
    "_Ham._": "Hamlet",
    "_Ros._": "Rosencrantz",
    "_Laer._": "Laertes",
    "_Osr._": "Osric",
    "_Oph._": "Ophelia",
    "_Pol._": "Polonius",
    "_Ghost._": "Ghost", # Ghost of Hamlet's Father
}

cast = list(abbreviations.values())

# 텍스트 파일 경로
txt_file_path = "./hamlet.txt" 

# 파일을 열고 내용 읽기
with open(txt_file_path, 'r', encoding='utf-8') as file:
    text_original = file.read()


# 원본 텍스트에서 약어를 바꾸는 과정
text_data = text_original
for abbr, full_name in abbreviations.items():
    # 특수문자를 안전하게 처리하기 위해 re.escape 사용
    text_data = re.sub(r'\b' + re.escape(abbr) + r'\b', full_name, text_data)


# "SCENE"을 기준으로 정규식으로 텍스트를 나누기
scenes = re.split(r'(?=SCENE)', text_data)  # SCENE을 포함하여 나누기

# 각 scene에 대해 'Notes'가 있으면 그 부분에서 다시 분할하기
scenes_and_notes = []
for scene in scenes:
    # Notes가 포함된 부분에서 분할
    subscenes = re.split(r'(?=Notes)', scene)
    scenes_and_notes.extend(subscenes)
scenes_and_notes = scenes_and_notes[1:]
print(len(scenes_and_notes))
print([len(text) for text in scenes_and_notes])
print('-'*100)

# 각 요소에서 첫 번째 줄바꿈을 기준으로 제목과 내용 분리
titles = [text.split('\n', 1)[0] for text in scenes_and_notes]
contents= [text.split('\n', 1)[1] for text in scenes_and_notes]
# contents에 대해 연속된 줄바꿈을 하나의 공백으로 처리하고, 여러 공백을 하나로 줄이는 전처리
processed_contents = [
    re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip() for text in contents
]
print('++'*50)
print(titles[1])
# print(contents[1])
#print(processed_contents[0])
print([len(c)for c in processed_contents])

# 첫 번째 줄을 key로, 전체 scene을 value로 하는 dictionary 만들기
chapters = dict(zip(titles, processed_contents))

# JSON 파일 구조 만들기
data = {
    "cast": cast,
    "chapters": chapters
}


# 현재 위치에 JSON 파일로 저장
json_file_path = './hamlet.json'

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)