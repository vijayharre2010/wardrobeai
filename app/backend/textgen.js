import OpenAI from "openai";

export async function POST(req) {
  try {
    const { userDetails } = await req.json();

    const openai = new OpenAI({
      apiKey: process.env.NVIDIA_API_KEY, // stored in .env.local
      baseURL: "https://integrate.api.nvidia.com/v1",
    });

    const completion = await openai.chat.completions.create({
      model: "mistralai/mixtral-8x22b-instruct-v0.1",
      messages: [
        {
          role: "system",
          content:
            "You are a professional fashion consultant specializing in functional, age-appropriate attire. Respond exclusively with a categorized outfit list in this exact format: 'Top: Brand item description\\nTop: Brand item description\\nBottom: Brand item description\\nShoes: Brand item description\\nAccessories: Brand item description' (use multiple Top lines for layering). Include reputable brands where suitable. Design a cohesive, aesthetically inspiring color theme using color theory principles (e.g., analogous or complementary schemes) to enhance the user's sporty style in extreme cold—prioritize warmth, mobility, and visual harmony with neutral bases and subtle accents for an empowering, modern athletic vibe. No explanations, no additional text.",
        },
        {
          role: "user",
          content: userDetails,
        },
      ],
      temperature: 0.7,
      top_p: 0.8,
      max_tokens: 256,
    });

    return new Response(
      JSON.stringify({ result: completion.choices[0].message.content }),
      { status: 200 }
    );
  } catch (error) {
    console.error("NVIDIA API Error:", error);
    return new Response(JSON.stringify({ error: "Failed to generate text" }), {
      status: 500,
    });
  }
}
