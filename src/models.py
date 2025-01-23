from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
model = model.eval()

# stars : from 1 to 5 with half-point
# sentiment_map = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}

def predict_sentiment(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    score = torch.argmax(probabilities, dim=-1).tolist()
    score_rescale = list(map(lambda x: x + 1, score))
    return score_rescale

def manage_scores(review_list):
    # compute sentiment score
    review_texts = [r['review'] for r in review_list]
    model_scores = predict_sentiment(review_texts)

    # clean ratings and add sentiment score
    for review, senti_score in zip(review_list, model_scores):
        try:
            review['rating'] = int(review['rating'][0])
        except ValueError:
            review['rating'] = -1
        
        review['star'] = senti_score
    
    return review_list


def get_avg_score(review_list):
    stars_avg = np.mean([r['star'] for r in review_list])
    rating_avg = np.mean([r['rating'] for r in review_list])
    return stars_avg, rating_avg
