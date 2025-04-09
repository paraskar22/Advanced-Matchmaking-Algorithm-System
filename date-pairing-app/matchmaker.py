from person import Person

class MatchMaker:
    def find_best_matches(self, people):
        """Find best matches and suggest alternatives if needed."""
        males = [p for p in people if p.gender == "Male"]
        females = [p for p in people if p.gender == "Female"]
        matches = {}

        # Pairing logic
        for female in females:
            best_match = None
            best_score = 0

            for male in males:
                if not female.is_compatible(male):
                    continue

                score = female.compatibility_score(male)
                if score > best_score:
                    best_match = male
                    best_score = score

            if best_match:
                matches[female.name] = {
                    "partner": best_match.name,
                    "score": best_score,
                    "religion": best_match.religion,
                    "profession": best_match.profession,
                    "personality_type": best_match.personality_type
                }
                males.remove(best_match)

        # Suggest better matches
        for female, match_info in matches.items():
            current_score = match_info["score"]
            for male in people:
                if male.name != match_info["partner"] and female.is_compatible(male):
                    new_score = next(f for f in people if f.name == female).compatibility_score(male)
                    if new_score > current_score:
                        matches[female]["suggested_alternative"] = male.name
                        matches[female]["new_score"] = new_score

        return matches

    def log_matches(self, matches):
        """Save matches to a file."""
        with open("matches.txt", "w") as f:
            for female, match_info in matches.items():
                partner = match_info["partner"]
                score = match_info["score"]
                alternative = match_info.get("suggested_alternative", "None")
                new_score = match_info.get("new_score", "N/A")

                f.write(f"{female} is matched with {partner} (Score: {score})\n")
                if alternative != "None":
                    f.write(f"  Suggested alternative: {alternative} (Score: {new_score})\n")
                f.write("\n")

        print("Matches saved to matches.txt")
