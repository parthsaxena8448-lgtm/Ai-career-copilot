import json

with open("skills.json", "r") as f:
    data = json.load(f)

print(data)
all_skills = []

for category_list in data.values():
    all_skills.extend(category_list)

print(all_skills)
with open("summary.txt", "w") as f:
    f.write(f"Total skills: {len(all_skills)}")