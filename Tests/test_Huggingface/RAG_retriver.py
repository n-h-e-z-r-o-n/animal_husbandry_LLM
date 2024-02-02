from langchain.document_loaders import TextLoader
from sentence_transformers import SentenceTransformer, util
from langchain.embeddings import SentenceTransformerEmbeddings

from langchain.text_splitter import CharacterTextSplitter
import torch
import joblib
loader = TextLoader('../animal_husbandry_LLM/DataSet/state_of_the_union.txt')
documents = loader.load()
print(documents)

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

print("No of Document pages: ", len(documents))
print("No of Document chunks: ", len(chunks))


corpus = []
for chunk in chunks:
    corpus.append(chunk.page_content)

# Using SentenceTransformers for embedding
embedder = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

joblib.dump(corpus_embeddings, '../DataStore/corpus_embeddings_np.joblib') # Save embeddings to a local file using joblib
joblib.dump(corpus, '../DataStore/corpus_data_list.joblib') # Save embeddings to a local file using joblib

loaded_embeddings = joblib.load('../DataStore/corpus_embeddings_np.joblib') # Load embeddings from the local file
loaded_corpus = joblib.load('../DataStore/corpus_data_list.joblib') # Load embeddings from the local file


def RAG_fun(query):

    query_embedding = embedder.encode(query, convert_to_tensor=True)  # get the embedding for the query

    # get the closest 5 documents to the query in embedding space.
    cos_scores = util.cos_sim(query_embedding, loaded_embeddings)[0]
    top_results = torch.topk(cos_scores, k=5)
    print(top_results)
    print("Query:", query, "\n Similar Documents:\n\n")
    m = None
    for score, idx in zip(top_results[0], top_results[1]):
        m = loaded_corpus[idx]
        print(loaded_corpus[idx])
        print(len(loaded_corpus[idx]))
        print("(Score: {})\n\n\n".format(score))
    return m

query = 'Why is proper housing important in animal husbandry'
answer = RAG_fun(query)
print(answer)