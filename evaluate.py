import re
import json
from nltk.translate.bleu_score import corpus_bleu
from rouge import Rouge
from langchain.chains import LLMChain
from langchain.llms import GradientLLM
from langchain.prompts import PromptTemplate
import os
import warnings

warnings.filterwarnings("ignore")

# ---------------------------- Access and Load the llm ----------------------------------------------------------------------------------------
# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "1vhvNKf2lLAMPvrOqhV97xaPPNRzwT1J"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

fine_tuned_Model_Id = "227859f1-11c4-41f9-ac14-31a287e1467a_model_adapter"  # initializes a GradientLLM with our fine-tuned model by specifying our model ID.

llm = GradientLLM(
    model=fine_tuned_Model_Id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""
prompt = PromptTemplate(template=template, input_variables=["Instruction"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# ------------------ Load the dataset ---------------------------------------------------------------------------------------------------------


with open("./DataSet/data.json") as f:  # Load the dataset from a JSON file
    samples = json.load(f)


# ----------------- Functions ---------------------------------------------------------------------------------------------------------------


def compute_rouge_scores(hypotheses, references):
    rouge = Rouge()
    scores = rouge.get_scores(hypotheses, references, avg=True)
    return scores


def compute_bleu_score(target_response, llm_responses):
    bleu_score = corpus_bleu([target_response.split()], [llm_responses.split()])  # Calculate BLEU score
    return bleu_score


def Find_Instruction(input_pattern, input_string):
    matches = re.findall(input_pattern, input_string, re.DOTALL)

    # If there are matches, extract the first one
    extracted_string = None
    if matches:
        extracted_string = matches[0]

    return extracted_string


def Evaluate(Sample=None, count=0):
    input_pattern = r'<s>### Instruction:\n(.*?) \n'
    response_pattern = r'Response:\n(.*?)</s>'
    bleu_scoreS = []
    rouge_scoreS = []

    if count != 0:
        iteration = count - 1
    else:
        iteration = count

    while iteration >= 0:

        input_query = Find_Instruction(input_pattern, Sample[iteration]["inputs"])
        target_response = Find_Instruction(response_pattern, samples[iteration]["inputs"])

        if input_query and target_response is not None:
            print("\n ---------------------------------------------------------------")
            print("INPUT QUERY:\n", input_query)
            print("\nTARGET RESPONSE:\n", target_response)

            llm_responses = llm_chain.run(Instruction=f"{input_query}")
            print("\nLLM RESPONSE:\n", llm_responses)

            rouge_scores = compute_rouge_scores(llm_responses, target_response)

            bleu_score = compute_bleu_score(target_response, llm_responses)
            print("\nBLEU Score:", bleu_score)
            print("ROUGE Scores:")
            print("\tROUGE-1 F1 Score:", rouge_scores["rouge-1"]["f"])
            print("\tROUGE-2 F1 Score:", rouge_scores["rouge-2"]["f"])
            print("\tROUGE-L F1 Score:", rouge_scores["rouge-l"]["f"])
            rouge_scoreS.append((rouge_scores["rouge-1"]["f"], rouge_scores["rouge-2"]["f"], rouge_scores["rouge-l"]["f"]))
            bleu_scoreS.append(bleu_score)


        iteration -= 1

    if count > 0:
        rouge_scores1 = 0
        rouge_scores2 = 0
        rouge_scores3 = 0
        bleu_scoreA = 0

        for i in bleu_scoreS:
            bleu_scoreA += i
        for i in rouge_scoreS:
            rouge_scores1 += i[0]
            rouge_scores2 += i[1]
            rouge_scores3 += i[2]

        print("\nAverageBLEU Score:", bleu_scoreA)
        print(f"Average ROUGE Scores for {count} samples")
        print("\tAverage ROUGE-1 F1 Score:", rouge_scores1 / count)
        print("\tAverage ROUGE-2 F1 Score:", rouge_scores2 / count)
        print("\tAverageROUGE-L F1 Score:", rouge_scores3 / count)

    print("\n ---------------------------------------------------------------")

Evaluate(Sample=samples, count=3)  # one sample evaluation



