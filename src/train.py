import sentience
import json

data = json.load(open("pm.json"))
model = sentience.create_model()

data = list(filter(lambda x: len(x["msg"])+len(x["ref"]) < 256, data))
for x in data:
    sentience.train(model, x["ref"], x["msg"])
