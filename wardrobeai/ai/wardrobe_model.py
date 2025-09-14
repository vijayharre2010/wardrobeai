# Placeholder AI logic
from g4f.client import Client

def suggest_outfit(weather, occasion):
    """
    Generate outfit suggestion based on weather and occasion.
    """
    suggestions = {
        "rainy": "a waterproof jacket and boots",
        "sunny": "a light t-shirt and shorts",
        "cold": "a warm coat and scarf",
        "formal": "a suit or formal dress",
        "casual": "jeans and a t-shirt"
    }

    outfit = []
    if weather.lower() in suggestions:
        outfit.append(suggestions[weather.lower()])
    else:
        outfit.append("comfortable clothes")

    if occasion.lower() in suggestions:
        outfit.append(suggestions[occasion.lower()])

    return " and ".join(outfit)

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
                    model="flux",  # Try a different model
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
