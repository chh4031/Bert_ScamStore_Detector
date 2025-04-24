import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import pandas as pd

# 기본모델 = bert-base-multilingual-cased
# monologg/kobert
# klue/bert-base
# monologg/koelectra-base-v3-discriminator
model_Name = 'monologg/koelectra-base-v3-discriminator'  # 모델 이름

# CSV 경로가 다를 경우 쓰는법
file_path = r'C:\Users\Slim7\Desktop\data\DATA_1000.csv'

# CSV 파일 읽는 부분 추가 => 외부 데이터 셋 가져오기(CSV 형식)
CSV_data = pd.read_csv(file_path)

# 학습 손실과 정확도를 저장할 리스트 초기화
train_losses = []
accuracies = []

# 데이터 준비
translated_sentences = CSV_data['translated_sentences'].tolist()
natural_sentences = CSV_data['natural_sentences'].tolist()
labels = CSV_data['labels'].tolist()

# 데이터 전처리
translated_sentences_len = int(len(translated_sentences)/2*-1)
natural_sentences_len = int(len(natural_sentences)/2)
translated_sentences = translated_sentences[:translated_sentences_len]
natural_sentences = natural_sentences[natural_sentences_len:]

# 데이터 전처리2
all_sentences = translated_sentences + natural_sentences
tokenizer = BertTokenizer.from_pretrained(model_Name)
encoded_all = tokenizer(all_sentences, padding='max_length', truncation=True, max_length=15, return_tensors='pt')

# 데이터셋 생성
input_ids = encoded_all['input_ids']
attention_masks = encoded_all['attention_mask']
labels = torch.tensor(labels)

# 학습 및 테스트 데이터 분리
train_inputs, test_inputs, train_labels, test_labels = train_test_split(input_ids, labels, test_size=0.33, random_state=42)
train_masks, test_masks, _, _ = train_test_split(attention_masks, attention_masks, test_size=0.33, random_state=42)

# 데이터 로더 생성
batch_size = 8
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_data = TensorDataset(test_inputs, test_masks, test_labels)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# 모델 초기화 및 GPU로 이동
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained(model_Name, num_labels=2)
# monologg/kobert, 기본모델 = bert-base-multilingual-cased, klue/bert-base, monologg/koelectra-base-v3-discriminator
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# 모델 학습
epochs = 10
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_dataloader:
        b_input_ids, b_input_mask, b_labels = batch
        b_input_ids, b_input_mask, b_labels = b_input_ids.to(device), b_input_mask.to(device), b_labels.to(device)
        model.zero_grad()
        outputs = model(b_input_ids, attention_mask=b_input_mask, labels=b_labels)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
    avg_train_loss = total_loss / len(train_dataloader)
    train_losses.append(avg_train_loss)
    print(f'Epoch {epoch+1}, Loss: {avg_train_loss:.4f}')

    # 모델 평가
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in test_dataloader:
            b_input_ids, b_input_mask, b_labels = batch
            b_input_ids, b_input_mask, b_labels = b_input_ids.to(device), b_input_mask.to(device), b_labels.to(device)
            outputs = model(b_input_ids, attention_mask=b_input_mask)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
            correct += (predictions == b_labels).sum().item()
            total += b_labels.size(0)
    accuracy = correct / total
    accuracies.append(accuracy)
    print(f'Accuracy: {accuracy:.4f}')

# 새로운 문장 테스트 => 이거 나중에 리뷰데이터 들고온거에서 가져올 수 있도록 해야함.(아직은 복잡해서 안해둠)
new_sentences = ["배송빠르고 제품 좋습니다 감사합니다 잘쓸게요",
                 "통관 과정잊 좀 오래걸리는거 빼면 좋음 ㅇㅇ", 
                 "동영상이나 웹셔핑으로는 훌륭합니다. 윈도우도 깔려있어서 따로 구하지 않아도 되서 좋네요. 가성비 최고입니다.",
                 "문제없이 잘 작동합니다. 배송도 빠르네요.", 
                 "잘받았습니다. 작동 잘됩니다.", 
                 "아직 사용해 보지 않았는데 좋네요",
                 "나는 그것을 좋아했다. 들어오지 않는 사무실 패키지 만 설치하면됩니다. 그러나", 
                 "최고의 제품! 이것을 구하기에 오래 걸렸습니다.", 
                 "좋은 품질. 최고의 제품. 나는 이것을 위해 기다렸습니다.",
                 "빠른 배송. 판매자는 매우 친숙합니다.", 
                 "판매자는 우리에게 최고의 제품을 선사합니다.",
                 "물건은 훌륭한 퀄리티를 자랑합니다."]

# 이 위에 데이터 크롤링한거 들어가야함
encoded_new = tokenizer(new_sentences, padding='max_length', truncation=True, max_length=15, return_tensors='pt')

model.eval()
with torch.no_grad():
    input_ids = encoded_new['input_ids'].to(device)
    attention_mask = encoded_new['attention_mask'].to(device)
    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=1)

sentence_number = 1
for sentence, prediction in zip(new_sentences, predictions):
    label = "번역된 문장       " if prediction.item() == 1 else "번역되지 않은 문장"
    # print(f"문장: {sentence} -> 예측: {label}")
    print(f"번호 : {sentence_number}, 예측결과 : {label} | {prediction.item()}, 사용된 문장 : {sentence}")
    sentence_number += 1

# 최종 epochs, 손실함수, 정확도 출력
print(f"전체 epochs = {epochs}, 최종 손실함수 : {avg_train_loss:.4f}, 최종 정확도 : {accuracy:.4f}")

# 전체 그래프 부분
plt.figure(figsize=(12, 5))

plt.suptitle(model_Name, fontsize=16)


# 손실함수 그래프
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs + 1), train_losses, marker='o')
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.ylim(0, 1)
plt.xlim(0.5, epochs + 0.5)

# 정확도 그래프 => 그래프로 시각적 표현을 위한 부분이라 따로 해석 없음
plt.subplot(1, 2, 2)
plt.plot(range(1, epochs + 1), accuracies, marker='o')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.xlim(0.5, epochs + 0.5)

plt.tight_layout()
plt.show()
