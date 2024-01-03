import torch
import json
from tqdm import tqdm
import torch.nn as nn
from torch.optim import Adam
import nltk
import spacy
import string
import evaluate  # Bleu
from torch.utils.data import Dataset, DataLoader, RandomSampler
import pandas as pd
import numpy as np
import transformers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from transformers import AutoModelForSeq2SeqLM, T5ForConditionalGeneration, T5TokenizerFast, AutoTokenizer

import warnings
#warnings.filterwarnings("ignore")

#  setting up the T5 model and the tokenizer, optimizer, and other hyperparameters for training.
model_name = "vblagoje/bart_lfqa"
MODEL = AutoModelForSeq2SeqLM.from_pretrained(model_name, return_dict=True)
TOKENIZER = AutoTokenizer.from_pretrained(model_name)

# Training Parameters for t5 models
#model_name = "t5-base"
#TOKENIZER = T5TokenizerFast.from_pretrained(model_name)
#MODEL = T5ForConditionalGeneration.from_pretrained(model_name, return_dict=True)


OPTIMIZER = Adam(MODEL.parameters(), lr=0.00001)
Q_LEN = 256  # Question Length
T_LEN = 256  # Target Length
BATCH_SIZE = 4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Device : ", DEVICE)


with open("../DataSet/unique_animal_husbandry_dataset.json") as f:
    custom_data = json.load(f)



def prepare_custom_data(data):
    articles    = []
    for block in data:

        inputs = {"question": block["question"], "answer": block["answer"]}
        articles.append(inputs)
    return articles

data = prepare_custom_data(custom_data)
data = pd.DataFrame(data)  # Create a Dataframe
print(data.head())



class QA_Dataset(Dataset):
    def __init__(self, tokenizer, dataframe, q_len, t_len):
        self.tokenizer = tokenizer
        self.q_len = q_len
        self.t_len = t_len
        self.data = dataframe
        self.questions = self.data["question"]
        #self.context = self.data["context"]
        self.answer = self.data['answer']

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        question = self.questions[idx]
        #context = self.context[idx]
        answer = self.answer[idx]

        #question_tokenized = self.tokenizer(question, context, max_length=self.q_len, padding="max_length", truncation=True, pad_to_max_length=True, add_special_tokens=True)
        question_tokenized = self.tokenizer(question, max_length=self.q_len, padding="max_length", truncation=True, pad_to_max_length=True, add_special_tokens=True)
        answer_tokenized = self.tokenizer(answer, max_length=self.t_len, padding="max_length",  truncation=True, pad_to_max_length=True, add_special_tokens=True)

        labels = torch.tensor(answer_tokenized["input_ids"], dtype=torch.long)
        labels[labels == 0] = -100

        return {
            "input_ids": torch.tensor(question_tokenized["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(question_tokenized["attention_mask"], dtype=torch.long),
            "labels": labels,
            "decoder_attention_mask": torch.tensor(answer_tokenized["attention_mask"], dtype=torch.long)
        }

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

train_sampler = RandomSampler(train_data.index)
val_sampler = RandomSampler(val_data.index)

qa_dataset = QA_Dataset(TOKENIZER, data, Q_LEN, T_LEN)

train_loader = DataLoader(qa_dataset, batch_size=BATCH_SIZE, sampler=train_sampler)
val_loader = DataLoader(qa_dataset, batch_size=BATCH_SIZE, sampler=val_sampler)

train_loss = 0
val_loss = 0
train_batch_count = 0
val_batch_count = 0


#MODEL.to(DEVICE)

epoch_count = 2
for epoch in range(epoch_count):
    MODEL.train()
    for batch in tqdm(train_loader, desc="Training batches"):
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)
        decoder_attention_mask = batch["decoder_attention_mask"].to(DEVICE)

        outputs = MODEL(
                          input_ids=input_ids,
                          attention_mask=attention_mask,
                          labels=labels,
                          decoder_attention_mask=decoder_attention_mask
                        )

        OPTIMIZER.zero_grad()
        outputs.loss.backward()
        OPTIMIZER.step()
        train_loss += outputs.loss.item()
        train_batch_count += 1

    #Evaluation
    MODEL.eval()
    for batch in tqdm(val_loader, desc="Validation batches"):
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)
        decoder_attention_mask = batch["decoder_attention_mask"].to(DEVICE)

        outputs = MODEL(
                          input_ids=input_ids,
                          attention_mask=attention_mask,
                          labels=labels,
                          decoder_attention_mask=decoder_attention_mask
                        )

        OPTIMIZER.zero_grad()
        outputs.loss.backward()
        OPTIMIZER.step()
        val_loss += outputs.loss.item()
        val_batch_count += 1

    print(f"\n\t{epoch+1}/{epoch_count} -> Train loss: {train_loss / train_batch_count}\tValidation loss: {val_loss/val_batch_count}")

MODEL.save_pretrained("qa_model")
TOKENIZER.save_pretrained("qa_tokenizer")