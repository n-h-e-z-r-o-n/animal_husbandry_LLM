# pip install -U gradient_haystack

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


document_store = InMemoryDocumentStore()
writer = DocumentWriter(document_store=document_store)

os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "b04a475d-65d1-4e98-82f2-62d218be3989_workspace"

document_embedder = GradientDocumentEmbedder(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
)

with open("./DataSet/data.json", 'r') as file:
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
    base_model_slug="llama2-7b-chat",
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


Query = "What is animal husbandry??"
# print(LLM_Run(Query))
