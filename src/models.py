from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)


def predict_sentiment(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    return torch.argmax(probabilities, dim=-1).tolist()


def compute_sentiment_score(poi):
    # compute sentiment analysis
    comments = [comment['text'] for comment in poi['comments']]
    sent_score = predict_sentiment(comments)

    # add it to the poi
    for comments, score in zip(poi['comments'], sent_score):
        comments['senti'] = score
    
    return poi

# stars : from 1 to 5 with half-point
# sentiment_map = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}
def get_avg_score(poi):
    stars_avg = np.mean([comments['stars'] for comments in poi['comments']])
    senti_avg = np.mean([comments.get('senti', -1) for comments in poi['comments']]) + 1

    return stars_avg, senti_avg
