import torch
from torch.optim import Adam
from transformers import T5ForConditionalGeneration, T5TokenizerFast, AutoModelForSeq2SeqLM, AutoTokenizer
import joblib
from sentence_transformers import SentenceTransformer, util

# TOKENIZER = T5TokenizerFast.from_pretrained("qa_tokenizer")
# MODEL = T5ForConditionalGeneration.from_pretrained("qa_model", return_dict=True)

#MODEL = AutoModelForSeq2SeqLM.from_pretrained("qa_model", return_dict=True)
#TOKENIZER = AutoTokenizer.from_pretrained("qa_tokenizer")

MODEL = AutoModelForSeq2SeqLM.from_pretrained("NousResearch/Nous-Hermes-Llama2-13b", return_dict=True) #lmsys/fastchat-t5-3b-v1.0
TOKENIZER = AutoTokenizer.from_pretrained("NousResearch/Nous-Hermes-Llama2-13b")



OPTIMIZER = Adam(MODEL.parameters(), lr=0.00001)
Q_LEN = 256  # Question Length
T_LEN = 250  # Target Length
BATCH_SIZE = 100
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL.to(DEVICE)
print("Fast Token : ", TOKENIZER.is_fast)
print("Device : ", DEVICE)

embedder = SentenceTransformer('all-MiniLM-L6-v2')  # get the embedding model
loaded_embeddings = joblib.load('../DataStore/corpus_embeddings_np.joblib') # Load embeddings from the local file
loaded_corpus = joblib.load('../DataStore/corpus_data_list.joblib') # Load embeddings from the local file


def RAG_fun(query):

    query_embedding = embedder.encode(query, convert_to_tensor=True)  # get the embedding for the query

    # get the closest 5 documents to the query in embedding space.
    cos_scores = util.cos_sim(query_embedding, loaded_embeddings)[0]
    top_results = torch.topk(cos_scores, k=5)
    print("Query:", query, "\n Similar Documents:\n\n")
    m = None
    for score, idx in zip(top_results[0], top_results[1]):
        m = loaded_corpus[idx]
        print("(Score: {})\n\n\n".format(score))
        break
    return m


def predict_answer(context, question, ref_answer=None):
    # inputs = TOKENIZER(question, max_length=Q_LEN, padding="max_length", truncation=True, add_special_tokens=True)
    inputs = TOKENIZER(question, max_length=Q_LEN, padding="max_length", truncation=True, add_special_tokens=True)
    input_ids = torch.tensor(inputs["input_ids"], dtype=torch.long).to(DEVICE).unsqueeze(0)
    attention_mask = torch.tensor(inputs["attention_mask"], dtype=torch.long).to(DEVICE).unsqueeze(0)
    outputs = MODEL.generate(input_ids=input_ids,
                             attention_mask=attention_mask,
                             min_length=10,
                             max_length=256,
                             do_sample=False,
                             early_stopping=True,
                             num_beams=8,
                             temperature=1.0,
                             top_k=None,
                             top_p=None,
                             eos_token_id=TOKENIZER.eos_token_id,
                             no_repeat_ngram_size=3,
                             num_return_sequences=1
                             )

    predicted_answer = TOKENIZER.decode(outputs.flatten(), skip_special_tokens=True)

    return predicted_answer


while True:
    print("Enter query")
    query = input("")

    if query == '0':
        break

    print(query)
    context = RAG_fun(query)
    print(" ===== :", context)

    m = predict_answer(context, query)
    print("Answer :", m, "\n\n")
