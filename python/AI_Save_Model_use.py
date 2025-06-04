import torch
from transformers import BertTokenizer, BertForSequenceClassification
import time

def Model(R_Data):

    start_time = time.time()

    # 저장된 경로
    save_directory = '../save'

    # 모델과 토크나이저 불러오기
    model = BertForSequenceClassification.from_pretrained(save_directory)
    tokenizer = BertTokenizer.from_pretrained(save_directory)

    # GPU로 이동 (필요시)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 평가 예시
    model.eval()

    # 실제 리뷰데이터가 들어가는 부분
    new_sentences = R_Data
    encoded_new = tokenizer(new_sentences, padding='max_length', truncation=True, max_length=15, return_tensors='pt')

    # 예측
    with torch.no_grad():
        input_ids = encoded_new['input_ids'].to(device)
        attention_mask = encoded_new['attention_mask'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1)
        # print(predictions)

        pred_list = predictions.tolist()
        print(pred_list)

        sentence_number = 1
        
    for sentence, prediction in zip(new_sentences, predictions):
        label = "번역된 문장       " if prediction.item() == 1 else "번역되지 않은 문장"
        # print(f"문장: {sentence} -> 예측: {label}")
        print(f"번호 : {sentence_number}, 예측결과 : {label} | {prediction.item()}, 사용된 문장 : {sentence}")
        sentence_number += 1

    end_time = time.time()
    check_time = end_time - start_time
    print(f"실행시간 : {check_time: .2f} 초")

    return pred_list