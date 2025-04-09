import json

class Person:
    def __init__(self, name, age, gender, hobbies, location, preferred_gender, min_age, max_age, religion, profession, personality_type):
        self.name = name
        self.age = age
        self.gender = gender
        self.hobbies = hobbies
        self.location = location
        self.preferred_gender = preferred_gender
        self.min_age = min_age
        self.max_age = max_age
        self.religion = religion
        self.profession = profession
        self.personality_type = personality_type

    def is_compatible(self, other):
        """Check if basic compatibility (age, gender, religion) is satisfied."""
        return (
            self.min_age <= other.age <= self.max_age and
            other.min_age <= self.age <= other.max_age and
            self.gender == other.preferred_gender and
            other.gender == self.preferred_gender and
            (self.religion == other.religion or self.religion == "Any" or other.religion == "Any")
        )

    def compatibility_score(self, other):
        """Calculate compatibility based on hobbies, profession, personality, etc."""
        if not self.is_compatible(other):
            return 0  # Incompatible match

        hobby_similarity = len(set(self.hobbies) & set(other.hobbies)) / max(len(set(self.hobbies)), 1)
        age_difference = 1 / (1 + abs(self.age - other.age))
        location_match = 1 if self.location == other.location else 0.5
        profession_match = 1 if self.profession == other.profession else 0.7
        personality_match = 1 if self.personality_type == other.personality_type else 0.6

        return (hobby_similarity * 0.3) + (age_difference * 0.2) + (location_match * 0.2) + (profession_match * 0.15) + (personality_match * 0.15)

    @staticmethod
    def load_people(json_file):
        """Load participants from a JSON file."""
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Person(**person) for person in data]
