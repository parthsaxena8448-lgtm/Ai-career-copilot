import json

# Create a dictionary of skills
skills_data = {
    "programming_languages": ["Python", "Java", "JavaScript"],
    "frameworks": ["React", "Django", "Streamlit"],
    "tools": ["Git", "Docker", "VS Code"],
    "databases": ["SQL", "MongoDB", "SQLite"]
}

# Save it as a JSON file
with open("skills.json", "w") as f:
    json.dump(skills_data, f, indent=4)

print("skills.json created!")