import requests

BASE = "http://127.0.0.1:5000"

# data = [{ "name": "Ficando milionario com 1 real", "views": 10000, "likes": 100}, 
#         { "name": "Ficando milionario com 2 real", "views": 100000, "likes": 100}, 
#         {"name": "Ficando milionario com 3 real", "views": 1000000, "likes": 100}]

# # mandando várias requisições 
# for i in range(len(data)):
#     response = requests.put(BASE + "/video/" + str(i), data[i])
#     print(response.json()) 

# input()
# response = requests.delete(BASE + "/video/0")
# print(response)                

# input()
response = requests.patch(BASE + "/video/2", {"views": 1})
print(response.json()) 
