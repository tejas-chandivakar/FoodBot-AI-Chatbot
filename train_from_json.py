import json
from collections import defaultdict

# Load JSON file
with open("training_responses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

intent_examples = defaultdict(list)
intent_responses = {}

for item in data:
    intent = item["intent"]
    example = item["example"]
    response = item["response"]

    intent_examples[intent].append(example)

    if intent not in intent_responses:
        intent_responses[intent] = response

# Generate NLU file
nlu_content = 'version: "3.1"\n\nnlu:\n\n'

for intent, examples in intent_examples.items():
    nlu_content += f'- intent: {intent}\n'
    nlu_content += '  examples: |\n'

    for ex in examples:
        nlu_content += f'    - {ex}\n'

    nlu_content += '\n'

with open("data/nlu.yml", "w", encoding="utf-8") as f:
    f.write(nlu_content)

# Generate Domain file
domain_content = 'version: "3.1"\n\n'
domain_content += 'intents:\n'

for intent in intent_examples.keys():
    domain_content += f'  - {intent}\n'

domain_content += '\nresponses:\n\n'

for intent, response in intent_responses.items():
    action_name = f"utter_{intent}"

    domain_content += f'  {action_name}:\n'
    domain_content += f'    - text: |\n'
    
    for line in response.split("\n"):
        domain_content += f'        {line}\n'

    domain_content += '\n'

with open("domain.yml", "w", encoding="utf-8") as f:
    f.write(domain_content)

# Generate Stories
stories_content = 'version: "3.1"\n\nstories:\n\n'

for intent in intent_examples.keys():
    stories_content += f'- story: {intent}_story\n'
    stories_content += '  steps:\n'
    stories_content += f'    - intent: {intent}\n'
    stories_content += f'    - action: utter_{intent}\n\n'

with open("data/stories.yml", "w", encoding="utf-8") as f:
    f.write(stories_content)

# Rules file
rules_content = '''version: "3.1"

rules:

- rule: fallback rule
  steps:
    - intent: nlu_fallback
    - action: utter_default
'''

with open("data/rules.yml", "w", encoding="utf-8") as f:
    f.write(rules_content)

print("✅ Training files generated successfully!")