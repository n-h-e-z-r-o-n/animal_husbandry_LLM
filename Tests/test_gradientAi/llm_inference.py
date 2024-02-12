
<<<<<<< HEAD:Tests/test_gradientAi/llm_inference.py
from langchain.chains import LLMChain
from langchain.llms import GradientLLM
from langchain.llms import GradientLLM
from langchain.prompts import PromptTemplate
import gradientai
import os


# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"


fine_tuned_Model_Id = "227859f1-11c4-41f9-ac14-31a287e1467a_model_adapter" #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.


llm = GradientLLM(
    model=fine_tuned_Model_Id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

Question = "What is animal husbandry?"

Answer = llm_chain.run(Instruction=f"{Question}")
print(Answer)



=======
>>>>>>> 06ab89fe95edfc88e75b4ebf3251b1e384fc268e:Test_LLM.py
