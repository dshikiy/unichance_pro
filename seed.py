import sys
import os
import random
from faker import Faker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine
import backend.models as models

fake = Faker()

# Создаем все таблицы
models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        print("🗑️ Очистка старых данных...")
        db.query(models.Application).delete()
        db.query(models.Scholarship).delete()
        db.query(models.Program).delete()
        db.query(models.University).delete()
        db.commit()

        countries_config = {
            "Italy": ["Rome", "Milan", "Turin", "Bologna", "Pisa", "Padua"],
            "Hungary": ["Budapest", "Debrecen", "Szeged", "Pécs"],
            "Germany": ["Munich", "Berlin", "Aachen", "Heidelberg", "Hamburg"],
            "Poland": ["Warsaw", "Krakow", "Wroclaw", "Poznan"],
            "Czechia": ["Prague", "Brno", "Ostrava"]
        }

        majors_list = [
            "Computer Science", "Data Science", "Artificial Intelligence",
            "Mechanical Engineering", "Civil Engineering", "Electrical Engineering",
            "Business Administration", "Economics", "International Relations",
            "Architecture", "Medicine", "Psychology", "Design"
        ]
        
        deadlines_list = ["2026-05-15", "2026-06-01", "2026-07-15", "2026-08-01"]

        print("🚀 Генерация 100 университетов...")
        all_programs = []

        for i in range(100):
            country = random.choice(list(countries_config.keys()))
            city = random.choice(countries_config[country])
            
            uni = models.University(
                name=f"{fake.company()} University of {city}" if i > 10 else f"{city} State University",
                country=country,
                city=city,
                description=f"Top-tier educational institution in {country}. Known for its research and international community.",
                website=f"https://www.{fake.domain_name()}"
            )
            db.add(uni)
            db.flush()

            num_programs = random.randint(3, 6)
            for _ in range(num_programs):
                major = random.choice(majors_list)
                degree = random.choice(["Bachelor", "Master"])
                
                min_ielts = random.choice([5.5, 6.0, 6.5, 7.0])
                min_gpa = round(random.uniform(2.5, 3.9), 1)
                min_sat = random.choice([1100, 1200, 1350, None]) if degree == "Bachelor" else None
                has_grant = True if country in ["Italy", "Hungary"] else random.choice([True, False, False])
                deadline = random.choice(deadlines_list)

                prog = models.Program(
                    university_id=uni.id,
                    name=major,
                    degree=degree,
                    min_ielts=min_ielts,
                    min_sat=min_sat,
                    gpa_min=min_gpa,
                    deadline=deadline,
                    has_full_grant=has_grant
                )
                db.add(prog)
                all_programs.append((prog, country))

        db.flush()

        print("💎 Добавление описаний грантов...")
        for prog, country in all_programs:
            if prog.has_full_grant:
                grant_desc = ""
                if country == "Italy":
                    grant_desc = "DSU Regional Grant: Covers tuition, accommodation, and 1 meal per day."
                elif country == "Hungary":
                    grant_desc = "Stipendium Hungaricum: Full tuition covered, monthly allowance, and health insurance."
                else:
                    grant_desc = "University Excellence Scholarship: 100% tuition waiver for international students."

                sch = models.Scholarship(
                    program_id=prog.id,
                    type="full",
                    description=grant_desc
                )
                db.add(sch)

        db.commit()
        print(f"✅ Успешно! Создано 100 университетов и {len(all_programs)} программ.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()