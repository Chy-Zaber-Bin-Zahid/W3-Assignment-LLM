import os
import requests
from typing import Optional, Tuple


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash-exp"
        

    def _make_request(self, prompt: str) -> Optional[str]:
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error found -> {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error found -> {str(e)}")
            return None


    def rewriteTitle(self, hotel) -> Optional[str]:
        prompt = f"""Rewrite this hotel property title to be more engaging and descriptive:
        Current Title: {hotel.property_title}
        Location: {hotel.city_name}
        Room Type: {hotel.room_type}
        Rating: {hotel.rating}/5
        
        Rules:
        1. Keep it concise but descriptive
        2. Include the location if relevant
        3. Highlight any unique features
        4. Maintain professionalism
        5. Return only the new title, no additional text
        """
        return self._make_request(prompt)
    

    def generateDescription(self, property_data) -> Optional[str]:
        prompt = f"""Generate an engaging hotel description:
        Hotel: {property_data['property_title']}
        Location: {property_data['city_name']}
        Room Type: {property_data['room_type']}
        Rating: {property_data['rating']}/5
        Price: ${property_data['price']} per night

        Write 2-3 paragraphs highlighting location, amenities, and value proposition.
        """
        return self._make_request(prompt)


    def generateSummary(self, property_data) -> Optional[str]:
        prompt = f"""Create a brief summary for this hotel:
        Name: {property_data['property_title']}
        Location: {property_data['city_name']}
        Price: ${property_data['price']}
        Rating: {property_data['rating']}/5
        Description: {property_data.get('description', 'Not available')}

        Create a concise 2-3 sentence summary highlighting key features.
        """
        return self._make_request(prompt)


    def generateReview(self, property_data) -> Tuple[Optional[float], Optional[str]]:
        prompt = f"""Generate a hotel review:
        Name: {property_data['property_title']}
        Location: {property_data['city_name']}
        Price: ${property_data['price']}
        Current Rating: {property_data['rating']}/5

        Format your response EXACTLY like this:
        RATING: [single number 1-5]
        REVIEW: [detailed review text]

        Note: The rating should be just a single number between 1 and 5.
        """
        response = self._make_request(prompt)
        if not response:
            return None, None
        try:
            parts = response.split('\n', 1)
            if len(parts) != 2:
                return None, None
            rating_part = parts[0].replace('RATING:', '').strip()
            try:
                rating = float(rating_part)
                rating = min(max(rating, 1), 5)
            except ValueError:
                return None, None
            review = parts[1].replace('REVIEW:', '').strip()
            return rating, review
        except Exception as e:
            print(f"Error found -> {str(e)}")
            return None, None
