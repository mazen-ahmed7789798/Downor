import requests

API_KEY = "3be540f9a18741afa81b9cb2ebdf68d8"
query = 'صفوة الصفوة'
url = "https://listen-api.listennotes.com/api/v2/search"

headers = {
    "X-ListenAPI-Key": API_KEY
}

params = {
    "q": query,       # الكلمة اللي هتبحث عنها
    "type": "podcast", # أو "episode" لو عايز تبحث عن حلقة محددة
    "limit": 5         # عدد النتائج
}

r = requests.get(url, headers=headers, params=params)
data = r.json()

results = data.get("results", [])[0]

# for key , value  in results[0].items():     
#     print(f"{key}: {value}")

print("Title:", results.get("title_original"))
print("Publisher:", results.get("publisher_original"))
print("Description:", results.get("description_original"))
print("Listen Notes URL:", results.get("listennotes_url"))
print("Total Episodes:", results.get("total_episodes"))
print("Image URL:", results.get("image"))
# print("RSS Feed:", results.get("rss"))