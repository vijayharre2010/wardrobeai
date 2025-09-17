# Placeholder AI logic
from g4f.client import Client
from g4f.Provider import LMArena
import yaml
import re

def suggest_outfit(weather, occasion, profile=None):
    """
    Generate outfit suggestion as a Python dict (parsed from YAML)
    based on weather, occasion, and optional user profile.
    """
    client = Client()
    
    # Build profile string if available
    profile_str = ""
    if profile:
        details = []
        if profile.get('age'):
            details.append(f"Age: {profile['age']}")
        if profile.get('gender'):
            details.append(f"Gender: {profile['gender']}")
        if profile.get('height'):
            details.append(f"Height: {profile['height']}")
        if profile.get('weight'):
            details.append(f"Weight: {profile['weight']}")
        if profile.get('ethnicity'):
            details.append(f"Ethnicity: {profile['ethnicity']}")
        if profile.get('style_preference'):
            details.append(f"Style preference: {profile['style_preference']}")
        if profile.get('extra_info'):
            details.append(f"Additional info: {profile['extra_info']}")
        if details:
            profile_str = f"""
User Profile:
- {'; '.join(details)}"""
    
    prompt = f"""
You are a styling assistant. For the input variables {weather} and {occasion}{', and user profile' if profile_str else ''}, output exactly one valid YAML document and nothing else (no explanations, no prose, no markdown fences). The YAML must follow this schema.

Schema:
outfit:
  top:
    brand: string|null
    item: string
    color: string
    fabric: string
    note: string|null
  bottom:
    brand: string|null
    item: string
    color: string
    fabric: string
    note: string|null
  shoes:
    brand: string|null
    item: string
    color: string
    material: string
    note: string|null
  accessories:
    brand: string|null
    item: string
    color: string
    material: string|null
    note: string|null

Rules:
1. Produce valid YAML only. Do not include anything before or after the YAML document.
2. Keep each text field concise (max ~8 words). "note" may be up to 20 words explaining why it fits the user.
3. Prioritize practicality for the specified {weather} and formality for the {occasion}.
4. Personalize based on user profile: consider body type (from height, weight, gender), skin tone/complexion (from ethnicity), preferred styles, and any additional info.
5. Use neutral to fashionable color names (e.g., "charcoal", "olive", "cream", "navy") that suit the user's profile.
6. For accessories, include 1–4 items; if none, return an empty list.
7. Provide exactly 3 tags.
8. If a field is irrelevant, set it explicitly to null (for strings) or [] (for lists).
9. No emojis, no lists outside the YAML, no extra keys.

Now output an outfit for:
weather: "{weather}"
occasion: "{occasion}"
{profile_str}
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        messages=[{"role": "user", "content": prompt}],
        web_search=True
    )

    raw_output = response.choices[0].message.content

    # Remove markdown code fences/backticks if present
    cleaned = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", raw_output.strip(), flags=re.MULTILINE)

    try:
        parsed = yaml.safe_load(cleaned)
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse YAML: {e}\n--- Raw Output ---\n{cleaned}")

    return parsed


def generate_outfit_images(prompt, style):
    """
    Generate 3 outfit images using g4f by calling the image API three times
    with slightly different prompts (base, front view, side view) and
    returning a list of dicts with url and alt text.
    """
    try:
        client = Client()
        images = []
        variations = [
            f"{prompt} in {style} style",
            f"{prompt} in {style} style, front view",
            f"{prompt} in {style} style, side view"
        ]
        for i, full_prompt in enumerate(variations):
            try:
                print(f"Attempting to generate image {i+1} with prompt: {full_prompt}")
                response = client.images.generate(
                    model="wardrobeai",  # Try a different model
                    prompt=full_prompt,
                    response_format="url"
                )

                images.append(response.data[0].url)

            except Exception as gen_e:
                # Log and continue to try the remaining variations
                print(f"Image generation iteration {i+1} failed for prompt '{full_prompt}': {gen_e}")
                continue
        print(f"Final images list: {images}")
        return images
    except Exception as e:
        print(f"Image generation error: {e}")
        import traceback
        traceback.print_exc()
        return []  # Return empty list on error

