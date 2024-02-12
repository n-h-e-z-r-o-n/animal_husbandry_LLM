
<<<<<<< HEAD:Tests/test_gradientAi/Retrieval_Augmented_Generation.py
from gradient_haystack.embedders.gradient_document_embedder import GradientDocumentEmbedder
from gradient_haystack.embedders.gradient_text_embedder import GradientTextEmbedder
from gradient_haystack.generator.base import GradientGenerator
from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.document_stores import InMemoryDocumentStore
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder
import os

os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"
fine_tuned_Model_Id = "227859f1-11c4-41f9-ac14-31a287e1467a_model_adapter"

document_store = InMemoryDocumentStore()
writer = DocumentWriter(document_store=document_store)


document_embedder = GradientDocumentEmbedder(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
)

with open("./DataSet/Raw_Text_Data.txt", encoding="utf-8") as file:
    text_data = file.read()

docs = [
    Document(content=text_data)
]

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(instance=document_embedder, name="document_embedder")
indexing_pipeline.add_component(instance=writer, name="writer")
indexing_pipeline.connect("document_embedder", "writer")
indexing_pipeline.run({"document_embedder": {"documents": docs}})

text_embedder = GradientTextEmbedder(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
)



generator = GradientGenerator(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
    model_adapter_id=fine_tuned_Model_Id,
    max_generated_token_count=350,
)

prompt = """You are helpful assistant ment to answer questions relating to animal husbandry. Answer the query, based on the
content in the documents. if you dont know the answer say you don't know.
{{documents}}
Query: {{query}}
\nAnswer:
"""

retriever = InMemoryEmbeddingRetriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt)

rag_pipeline = Pipeline()
rag_pipeline.add_component(instance=text_embedder, name="text_embedder")
rag_pipeline.add_component(instance=retriever, name="retriever")
rag_pipeline.add_component(instance=prompt_builder, name="prompt_builder")
rag_pipeline.add_component(instance=generator, name="generator")
rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
rag_pipeline.connect("generator.replies", "answer_builder.replies")
rag_pipeline.connect("retriever", "answer_builder.documents")
rag_pipeline.connect("text_embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "generator")


def LLM_Run(question):
    result = rag_pipeline.run(
        {
            "text_embedder": {"text": question},
            "prompt_builder": {"query": question},
            "answer_builder": {"query": question}
        }
    )
    return result["answer_builder"]["answers"][0].data


Query = "When is diarrhoea very risky???"
print(LLM_Run(Query))
=======
>>>>>>> 06ab89fe95edfc88e75b4ebf3251b1e384fc268e:RAG.py
