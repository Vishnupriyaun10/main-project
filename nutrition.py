import requests
def view(name):
    query = name
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'RYng6UHZkKAxNHjm9LNiTw==EeDMmMUjHqOEpGYN'})
    if response.status_code == requests.codes.ok:
        print("hee",response.text)

        p=response.text.replace("[","").replace("]","").replace("{","").replace("}","").replace("name","").replace("calories","").replace("serving_size_g","").replace("fat_total_g","").replace("fat_saturated_g","").replace("protein_g","").replace("sodium_mg","").replace("potassium_mg","").replace("cholesterol_mg","").replace("carbohydrates_total_g","").replace("fiber_g","").replace("sugar_g","") .replace('"',"").replace(":","").replace(" ","")
        print("hello ",p)
        p=p.split(",")
        print(p)
        return p
    else:
        print("Error:", response.status_code, response.text)
        return "Error"
view("apple pie")