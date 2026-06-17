from decimal import Decimal


def calculate_match_score(candidate_skills, required_skills, candidate_experience, required_experience):
    required = {skill.strip().lower() for skill in required_skills if skill.strip()}
    candidate = {skill.strip().lower() for skill in candidate_skills if skill.strip()}

    if not required:
        skill_score = 0
    else:
        matched = required.intersection(candidate)
        skill_score = (len(matched) / len(required)) * 80

    if required_experience == 0:
        experience_score = 20
    else:
        experience_score = min(candidate_experience / required_experience, 1) * 20

    return Decimal(str(round(skill_score + experience_score, 2)))
