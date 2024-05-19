import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(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)

file_path = '../assets/Metrics.csv'
df = pd.read_csv(file_path)
df.rename(columns={'Metric ': 'Metric'}, inplace=True)
metrics_list = df['Metric']
metrics_string = ", ".join(metrics_list)

question = "If you woke up one morning, and all humans on Earth had disappeared out of thin air, what would you do?"
answer = "I would immediately search for the answer, as this occurrence demands answers, in case there is a way that I can revert this. I would leave my house and make way for the first high human denstiny area in search for others (if any are left). Afterwards, I would go to the library and take books on all key human findings throughout history, create a collection across all disciplines and safeguard it, in the case of mass destruction in order to retain human knowledge. I would, using my skills in technology design and build a safe living fortress, with automatic defences in the case of attack from wildlife or more sinister creatures. Here, I would safeguard mankind's knowledge and slowly work to unravel the reason behind human disappearance."
# We can later use something like this to test differnet answers:
# answer = input("Enter your answer: ")


completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assessor to a question on a test, your job is to assign a score between 1 and 10 for each of the 40 metrics provided to you for an answer to a test question"},
        {"role": "user", "content": f"Given the following metrics: {metrics_string}. You are tasked with the job of assessing an applicant who answered the question: {question} with the answer: {answer}. In your response, don't give me any explanations, just provide me with each metric and the answer's score for each. separate each metric name and number with a : so i can deal with it easily in my code"}
    ]
)

scores = completion.choices[0].message

# Convert user scores into a Dataframe so they can be used by nnKDtree
scores_dict = dict(item.split(": ") for item in scores.split(", "))
scores_df = pd.DataFrame(list(scores_dict.items()), columns=['Metric', 'Score'])
scores_df['Score'] = scores_df['Score'].astype(int)

# tempoary for testing -> save DataFrame to CSV file 
scores_df.to_csv('../assets/UserScores.csv', index=False)