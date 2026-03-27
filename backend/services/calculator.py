def calculate_chance(user, program):
    ielts_ratio = user.ielts / program.min_ielts
    sat_ratio = (user.sat / program.min_sat) if user.sat and program.min_sat else 1
    gpa_ratio = user.gpa / program.min_gpa

    score = 0.4 * ielts_ratio + 0.4 * sat_ratio + 0.2 * gpa_ratio
    chance = min(round(score * 100, 1), 100)

    if chance >= 80:
        level = "High"
    elif chance >= 60:
        level = "Medium"
    else:
        level = "Low"

    return chance, level