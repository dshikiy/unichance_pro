from sqlalchemy.orm import Session
from backend.models import Program, University
from backend.schemas import UserRequest

def normalize_ratio(user_value, required_value):
    """Нормализация показателей от 0 до 1.2"""
    if not required_value or required_value == 0:
        return 1.0
    if not user_value:
        return 0.5
    return min(user_value / required_value, 1.2)

def calculate_chance_score(user_ielts, user_sat, user_gpa, min_ielts, min_sat, min_gpa):
    """Расчет шанса на поступление в процентах"""
    ielts_score = normalize_ratio(user_ielts, min_ielts)
    sat_score = normalize_ratio(user_sat, min_sat) if min_sat else 1.0
    gpa_score = normalize_ratio(user_gpa, min_gpa)

    total_score = (ielts_score * 0.4) + (sat_score * 0.4) + (gpa_score * 0.2)
    chance = max(0, min(round(total_score * 100, 1), 100))

    if chance >= 80:
        level = "High"
    elif chance >= 60:
        level = "Medium"
    else:
        level = "Low"

    return chance, level

def get_calculated_programs(db: Session, user: UserRequest):
    """Поиск подходящих программ и расчет шансов"""
    query = db.query(Program).join(University)

    if user.country and user.country.lower() != "any":
        query = query.filter(University.country.ilike(f"%{user.country.strip()}%"))

    if user.major:
        query = query.filter(Program.name.ilike(f"%{user.major.strip()}%"))

    if user.require_full_grant:
        query = query.filter(Program.has_full_grant == True)

    programs = query.all()
    results = []

    for prog in programs:
        chance, level = calculate_chance_score(
            user.ielts, user.sat, user.gpa,
            prog.min_ielts, prog.min_sat, prog.gpa_min
        )

        results.append({
            "program_id": prog.id,
            "university_name": prog.university.name,
            "university_country": prog.university.country,
            "university_city": prog.university.city,
            "university_website": prog.university.website,
            "program_name": prog.name,
            "degree": prog.degree,
            "chance": chance,
            "level": level,
            "has_full_grant": prog.has_full_grant,
            "deadline": prog.deadline
        })

    # Сортируем от самого высокого шанса к низкому
    results.sort(key=lambda x: x["chance"], reverse=True)
    return results

def get_university_details(db: Session, uni_id: int):
    """Получение детальной информации об университете"""
    return db.query(University).filter(University.id == uni_id).first()