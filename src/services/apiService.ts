// API service for WardrobeAI

// Base URL for API calls (update this to your actual deployment URL)
const API_BASE_URL = 'http://localhost:8101'; // Change this to your Vercel deployment URL

// Generate outfit based on user details
export async function generateOutfit(userDetails: any): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/textgen`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userDetails }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error generating outfit:', error);
    throw error;
  }
}

// Generate outfit image based on outfit description
export async function generateOutfitImage(prompt: string): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/imggen`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.imageUrl;
  } catch (error) {
    console.error('Error generating outfit image:', error);
    throw error;
  }
}