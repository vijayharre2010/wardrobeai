import sys
import json
from g4f.client import Client

client = Client()

with open("prompt.txt") as f:
    system_prompt = f.read()

# Accept userDetails from Node
user_details = sys.argv[1] if len(sys.argv) > 1 else "default details"

response = client.chat.completions.create(
    model="moonshotai/Kimi-K2-Instruct",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_details},
    ],
)

outfit_json = response.choices[0].message.content.strip()

try:
    outfit = json.loads(outfit_json)
    # Print JSON so Node can read it
    print(json.dumps(outfit, indent=2))
except json.JSONDecodeError:
    print(outfit_json)
    sys.exit(1)
