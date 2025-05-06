# pip install google-genai
Gem_Key = 'AIzaSyBVyxW7Hrsjp_X8zITdRKDyri308xCM6ig'
from google import genai

client = genai.Client(api_key=Gem_Key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)


prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
)

# Use the response as a JSON string.
print(response.text)