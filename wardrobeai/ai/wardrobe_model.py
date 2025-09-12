# Placeholder AI logic
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
