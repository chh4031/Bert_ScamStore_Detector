import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

# 학습 손실과 정확도를 저장할 리스트 초기화
train_losses = []
accuracies = []

# 데이터 준비 (예시 데이터)
translated_sentences = ["이것은 예입니다.", "이것은 또 다른 예입니다.", "이것은 번역된 문장입니다.", "이것은 중국어에서 번역된 문장입니다."]
natural_sentences = ["이 문장은 자연스러운 한국어임.", "이 문장은 번역되지 않은 자연스러운 문장임.", "이 문장은 매우 자연스러움.", "이 문장은 한국어로 작성되었습니다."]
labels = [1, 1, 1, 1, 0, 0, 0, 0]  # 1: 번역된 문장, 0: 자연스러운 문장

# 데이터 전처리
all_sentences = translated_sentences + natural_sentences
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
encoded_all = tokenizer(all_sentences, padding='max_length', truncation=True, max_length=10, return_tensors='pt')

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

# 모델 초기화
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# 모델 학습
epochs = 3
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
    print(f'Epoch {epoch+1}, Loss: {avg_train_loss:.4f}')

# 모델 평가
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
print(f'Accuracy: {accuracy:.4f}')

# 새로운 문장 테스트
new_sentences = ["이것은 번역된 문장입니다..", "이것은 번역되지 않았음."]
encoded_new = tokenizer(new_sentences, padding='max_length', truncation=True, max_length=10, return_tensors='pt')

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

# AI_ex1_kobert랑 같은 코드지만 kobert가 아닌 기본 bert 사용했다는 점이 다름
# 파이썬 3.13 버전 로컬환경에서 실행할것.