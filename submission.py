import json
import random

# Load keywords from the provided file
with open('keywords.py') as file:
    file_content = file.read()

# Extract JSON part
start_index = file_content.find('[')
end_index = file_content.rfind(']') + 1
keywords_json_str = file_content[start_index:end_index]

# Parse JSON
keywords = json.loads(keywords_json_str)

# Organize keywords by category
keyword_dict = {}
for category_data in keywords:
    category = category_data["category"]
    words = category_data["words"]
    keyword_dict[category] = {word["keyword"]: word["alts"] for word in words}

# Example keyword the answerer is thinking of
answerer_category = random.choice(list(keyword_dict.keys()))
answerer_word = random.choice(list(keyword_dict[answerer_category].keys()))

# Memory structure to track interactions
guesser_memory = {
    "questions": [],
    "answers": [],
    "categories": []
}

# Agent logic for the guesser
def guesser_agent(observation, configuration):
    if observation["turnType"] == "ask":
        # Choose a category not yet confirmed
        possible_categories = list(keyword_dict.keys())
        if guesser_memory["categories"]:
            possible_categories = [cat for cat in possible_categories if cat not in guesser_memory["categories"]]

        if not possible_categories:
            possible_categories = list(keyword_dict.keys())

        category = random.choice(possible_categories)
        question = f"Is it related to {category}?"
        guesser_memory["questions"].append(question)
        return question

    elif observation["turnType"] == "guess":
        # Make a guess based on the confirmed category
        confirmed_category = None
        if "yes" in guesser_memory["answers"]:
            confirmed_category = guesser_memory["categories"][guesser_memory["answers"].index("yes")]
        if not confirmed_category:
            confirmed_category = random.choice(list(keyword_dict.keys()))
        
        guess = random.choice(list(keyword_dict[confirmed_category].keys()))
        guesser_memory["questions"].append(guess)
        return guess

# Agent logic for the answerer
def answerer_agent(observation, configuration):
    if observation["turnType"] == "answer":
        question = observation["questions"][-1]
        category = question.split()[-1][:-1]  # Extract category from question
        guesser_memory["categories"].append(category)
        if category == answerer_category:
            answer = "yes"
        else:
            answer = "no"
        guesser_memory["answers"].append(answer)
        return answer

# Define the agent function required by the environment
def agent(observation, configuration):
    if observation["role"] == "guesser":
        return guesser_agent(observation, configuration)
    else:
        return answerer_agent(observation, configuration)
