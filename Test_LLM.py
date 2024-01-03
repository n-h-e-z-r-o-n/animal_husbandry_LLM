# pip install langchain-community
# pip install -U langchain

from langchain.chains import LLMChain
from langchain.llms import GradientLLM
from langchain.llms import GradientLLM
from langchain.prompts import PromptTemplate
import gradientai
import os

# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "b04a475d-65d1-4e98-82f2-62d218be3989_workspace"


fine_tuned_Model_Id = "4f2d6d3c-4685-493d-b945-08da7f120021_model_adapter"

#  initializes a GradientLLM with our fine-tuned model by specifying our model ID.
llm = GradientLLM(
    model = fine_tuned_Model_Id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

Question = "Discuss the role of nutrition in animal husbandry"

#Answer = llm_chain.run(Instruction=Question)
#print(Answer)