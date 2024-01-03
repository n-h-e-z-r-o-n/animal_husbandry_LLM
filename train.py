# ===================== PACKAGES USED IN THIS FILE ==============================================================================
# pip install gradientai --upgrade
# pip install langchain

# ====================== IMPORTS =================================================================================================
import json
import os
from gradientai import Gradient
from langchain.chains import LLMChain
from langchain.llms import GradientLLM
from langchain.prompts import PromptTemplate

os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "b04a475d-65d1-4e98-82f2-62d218be3989_workspace"


# ========================== LOADING THE DATASET AND DIVIDING IT INTO CHUNKS =====================================================
def divide_into_chunks(number, chunk_size):
    chunks = []

    while number > 0:
        if number >= chunk_size:
            chunks.append(chunk_size)
            number -= chunk_size
        else:
            chunks.append(number)
            break

    return chunks


with open("/content/data.json") as f:
    samples = json.load(f)

chunks = divide_into_chunks(len(samples), 100)
print(chunks)

# =============================== FINE TUNING THE MODEL ============================================================================

with Gradient() as gradient:
    base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
    new_model_adapter = base_model.create_model_adapter(name="Animal_husbandry-LLM(hezron)")
    print(f"Created model adapter with id {new_model_adapter.id}")

    num_epochs = 3  # num_epochs is the number of times you fine-tune the model # more epochs tends to get better results, but you also run the risk of "overfitting"
    count = 0
    while count < num_epochs:
        print(f"Fine-tuning the model, iteration {count + 1}")
        s = 0
        n = 1
        for i in chunks:
            print(f"chunk {n} range: {s} : {(s + i)}")
            while True:
                try:
                    new_model_adapter.fine_tune(samples=samples[s: (s + i)])
                    break
                except:
                    pass
            s += i
            n += 1
        count = count + 1


# ==================================== TESTING THE FINE_TUNED MODEL ====================================================================

llm = GradientLLM(

    model=new_model_adapter.id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])
answer = llm_chain = LLMChain(prompt=prompt, llm=llm)
print(answer)
