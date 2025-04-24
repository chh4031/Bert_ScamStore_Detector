"""
전체 코드에 대한 해석은 노션 참고
감정 기반 KoBert 쓰는 코드에서 좀 변형을 해서 만들어냄

데이터 셋을 csv로 저장해서 가져오는 방식 존재함 => 나중에 추가
모델을 저장해서 (.pt 형태) 사용하는 방식도 존재함 => 나중에 추가
==> 일단 데이터 셋을 우선적으로 구해서 학습을 시키고, 이를 바탕으로 손실이 가장 적은 모델이 나왔을때
해당 모델을 저장시켜서 불러와서 사용하면 학습하는 코드가 필요하지 않으므로, 계산 시간 단축 => 효율 증가
이거 쿠다 지금 cpu로 돌려서 좀 느림 => egpu 오면 쿠다 사용해서 할것!
"""


import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import pandas as pd

# CSV 경로가 다를 경우 쓰는법
file_path = r'C:\Users\Slim7\Desktop\DATA_1000.csv'

# CSV 파일 읽는 부분 추가 => 외부 데이터 셋 가져오기(CSV 형식)
# CSV_data = pd.read_csv('databackup.csv')
CSV_data = pd.read_csv(file_path)

# 학습 손실과 정확도를 저장할 리스트 초기화 (노션 1번항목)
train_losses = []
accuracies = []

# 데이터 준비 (예시 데이터) (노션 2번항목)

# 외부 csv 데이터셋 들고오기
# CSV_data['translated_sentences'] = CSV_data['translated_sentences'].fillna('')  # NaN 값을 빈 문자열로 대체
# CSV_data['natural_sentences'] = CSV_data['natural_sentences'].fillna('')  # NaN 값을 빈 문자열로 대체

# CSV_data = CSV_data.dropna(subset=['translated_sentences', 'natural_sentences']) # nan 값 제거

# CSV_data = CSV_data.applymap(lambda x: None if pd.isna(x) else x) # nan이 있는 셀만 제거

# 디버그용
# print(CSV_data)

translated_sentences = CSV_data['translated_sentences'].tolist()
natural_sentences = CSV_data['natural_sentences'].tolist()
labels = CSV_data['labels'].tolist()

# 데이터셋을 슬라이스 하기 위한 데이터, 리스트형식이라 슬라이스 될듯 => 데이터안맞을때 할것. 지금은 데이터 맞음 하지마셈.
translated_sentences_len = int(len(translated_sentences)/2*-1)
natural_sentences_len = int(len(natural_sentences)/2)

# 디버그용
# print(translated_sentences)
# print(natural_sentences)
# print(translated_sentences_len)
# print(natural_sentences_len)
# print(translated_sentences[:translated_sentences_len])
# print(natural_sentences[natural_sentences_len:])
# print(len(translated_sentences[:translated_sentences_len]))
# print(len(natural_sentences[natural_sentences_len:]))
# print(labels[0:101])
# print(labels[101:])
# print(labels)
# print(len(labels))

# 데이터 전처리1 => 이거는 각 데이터들이 nan값이 있어서 잘라내는 부분
translated_sentences = translated_sentences[:translated_sentences_len]
natural_sentences = natural_sentences[natural_sentences_len:]

# # 내부에서 데이터 쓰기
# translated_sentences = ["고품질의 제품! 지금까지 나는 불평할 것이 없습니다. 매우 빠르고 안정적이며 컴팩트합니다.", "훌륭한 기계. 시스템의 충전 속도는 매우 빠릅니다. 집에서 샀어요.", "훌륭한 제품. 작은 크기. 매우 빠르다. 내 일상 업무에 충분합니다.", "내가 여기서 물건을 산 것은 이번이 처음이다. 모든 것이 순조롭다. 지금까지 모든 것이 문제없다.", "조용하고 컴팩트하며 뛰어난 성능으로 비디오 시청 및 웹 탐색에 적합합니다."]
# natural_sentences = ["오늘 작동 시켜봤는데 잘되네요 오래썻으면 합니다", "배송 빠르고 상품 문제 없이 잘 도착했습니다. 작동 잘 되고 듀얼 모니터도 잘 되네요. 풀로드시 팬 소음은 있어요.", "너무잘되요 동봉도니 hdmi는 가끔 인식오류떠서 다른거 쓰니 잘되요", "괜찬은 재품입니다. 좋아요", "아주좋아요ㅠ생각보다 빨라요"]
# labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]


""" # 데이터 바꾼다고 주석처리
translated_sentences = ["이것은 예입니다.", "이것은 또 다른 예입니다.", "이것은 번역된 문장입니다.", "이것은 중국어에서 번역된 문장입니다."]
natural_sentences = ["이 문장은 자연스러운 한국어임.", "이 문장은 번역되지 않은 자연스러운 문장임.", "이 문장은 매우 자연스러움.", "이 문장은 한국어로 작성되었습니다."]
labels = [1, 1, 1, 1, 0, 0, 0, 0]  # 1: 번역된 문장, 0: 자연스러운 문장 => 라벨 2개임"
"""

# 데이터 전처리2 (노션 3번항목)
all_sentences = translated_sentences + natural_sentences
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
encoded_all = tokenizer(all_sentences, padding='max_length', truncation=True, max_length=15, return_tensors='pt')

# 디버그용
# print(all_sentences)

# 데이터셋 생성 (노션 4번항목)
input_ids = encoded_all['input_ids']
attention_masks = encoded_all['attention_mask']
labels = torch.tensor(labels)

# 학습 및 테스트 데이터 분리 (노션 5번항목)
train_inputs, test_inputs, train_labels, test_labels = train_test_split(input_ids, labels, test_size=0.33, random_state=42)
train_masks, test_masks, _, _ = train_test_split(attention_masks, attention_masks, test_size=0.33, random_state=42)

# 데이터 로더 생성 (노션 6번항목)
batch_size = 8
train_data = TensorDataset(train_inputs, train_masks, train_labels)

train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_data = TensorDataset(test_inputs, test_masks, test_labels)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# 모델 초기화 (노션 7번항목)
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# 모델 학습 (노션 8번항목)
epochs = 5
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_dataloader:
        b_input_ids, b_input_mask, b_labels = batch
        model.zero_grad()
        outputs = model(b_input_ids, attention_mask=b_input_mask, labels=b_labels)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
    avg_train_loss = total_loss / len(train_dataloader)
    train_losses.append(avg_train_loss)
    print(f'Epoch {epoch+1}, Loss: {avg_train_loss:.4f}')

    # 모델 평가 (노션 9번항목)
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in test_dataloader:
            b_input_ids, b_input_mask, b_labels = batch
            outputs = model(b_input_ids, attention_mask=b_input_mask)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
            correct += (predictions == b_labels).sum().item()
            total += b_labels.size(0)
    accuracy = correct / total
    accuracies.append(accuracy)
    print(f'Accuracy: {accuracy:.4f}')


# 새로운 문장 테스트 (노션 10번항목)

new_sentences = ["배송빠르고 제품 좋습니다 감사합니다 잘쓸게요", "동영상이나 웹셔핑으로는 훌륭합니다. 윈도우도 깔려있어서 따로 구하지 않아도 되서 좋네요. 가성비 최고입니다.", "잘받았습니다. 작동 잘됩니다.", "나는 그것을 좋아했다. 들어오지 않는 사무실 패키지 만 설치하면됩니다. 그러나", "최고의 제품! 이것을 구하기에 오래 걸렸습니다.", "좋은 품질. 최고의 제품. 나는 이것을 위해 기다렸습니다."]
encoded_new = tokenizer(new_sentences, padding='max_length', truncation=True, max_length=15, return_tensors='pt')

""" # 이 부분도 테스트를 위한 부분임 , 원본은 백업
new_sentences = ["이것은 번역된 문장입니다.", "이것은 번역되지 않았음."]
encoded_new = tokenizer(new_sentences, padding='max_length', truncation=True, max_length=10, return_tensors='pt')
"""

model.eval()
with torch.no_grad():
    input_ids = encoded_new['input_ids']
    attention_mask = encoded_new['attention_mask']
    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=1)

for sentence, prediction in zip(new_sentences, predictions):
    label = "번역된 문장" if prediction.item() == 1 else "번역되지 않은 문장"
    print(f"문장: {sentence} -> 예측: {label}")


# 이 부분은 손실과 평균값을 각 에포크에 따라 어떻게 달라지는지 확인을 위해 필요한 코드임
# 학습 손실 그래프 => 그래프로 시각적 표현을 위한 부분이라 따로 해석 없음
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs + 1), train_losses, marker='o')
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# 정확도 그래프 => 그래프로 시각적 표현을 위한 부분이라 따로 해석 없음
plt.subplot(1, 2, 2)
plt.plot(range(1, epochs + 1), accuracies, marker='o')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

plt.tight_layout()
plt.show()
