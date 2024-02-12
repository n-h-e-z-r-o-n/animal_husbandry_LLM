
<<<<<<< HEAD
# ====================== IMPORTS =================================================================================================
import json
import os
from gradientai import Gradient
from langchain.chains import LLMChain
from langchain.llms import GradientLLM
from langchain.prompts import PromptTemplate

# Set the environment variables for gradient.ai using your access token and workspace ID
os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

# ========================== LOADING THE DATASET AND DIVIDING IT INTO CHUNKS =====================================================

def divide_into_chunks(number, chunk_size):  # Define a function to divide a number into chunks of a given size
    chunks = []
    while number > 0:
        if number >= chunk_size:
            chunks.append(chunk_size)
            number -= chunk_size
        else:
            chunks.append(number)
            break

    return chunks


with open("./DataSet/data.json") as f:  # Load the dataset from a JSON file
    samples = json.load(f)


Batches = divide_into_chunks(len(samples), 100)  # Divide the dataset into chunks of 100 samples each
print(Batches)

# =============================== FINE TUNING THE MODEL ============================================================================

# Create a Gradient object to interact with gradient.ai
with Gradient() as gradient:
    base_model = gradient.get_base_model(base_model_slug="nous-hermes2") # base model Nous-Hermes-Llama2-13b
    new_model_adapter = base_model.create_model_adapter(
        name="Llama2-13b/Animal_Husbandry",
        learning_rate=0.00005,
        rank=8
    )

    print(f"Created model adapter with id {new_model_adapter.id}")
    num_epochs = 1  # num_epochs is the number of times you fine-tune the model # more epochs tends to get better results, but you also run the risk of "overfitting"
    count = 0
    while count < num_epochs:
        print(f"Fine-tuning the model, iteration {count + 1}")
        s = 0
        n = 1
        for Batch in Batches:
            print(f"chunk {n} range: {s} : {(s + i)}")
            while True:
                try:  # Try to fine-tune the model with the chunk of samples, If an error occurs, retry
                    metric = new_model_adapter.fine_tune(samples=samples[s: (s + Batch)])
                    print(f"\n Batch {n} Evaluation :", metric)
                    break
                except:
                    pass
            s += Batch
            n += 1
        count = count + 1

# ==================================== TESTING THE FINE_TUNED MODEL ====================================================================
# Create a GradientLLM object with the fine-tuned model ID and the maximum number of tokens to generate

llm = GradientLLM(

    model=new_model_adapter.id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = "### Instruction: {Instruction} \n\n### Response:"
prompt = PromptTemplate(template=template, input_variables=["Instruction"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What types of car batteries do you offer?"
answer = llm_chain.run(Instruction=question)
print(answer)
=======
>>>>>>> 06ab89fe95edfc88e75b4ebf3251b1e384fc268e
