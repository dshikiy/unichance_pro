import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine
import backend.models as models

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

        # НАҒЫЗ ЕУРОПА УНИВЕРСИТЕТТЕРІНІҢ ТІЗІМІ
        REAL_UNIS = [
            # Italy
            ("Sapienza University of Rome", "Italy", "Rome"),
            ("Politecnico di Milano", "Italy", "Milan"),
            ("University of Bologna", "Italy", "Bologna"),
            ("University of Padua", "Italy", "Padua"),
            ("Politecnico di Torino", "Italy", "Turin"),
            ("University of Pisa", "Italy", "Pisa"),
            ("University of Milan", "Italy", "Milan"),
            # Germany
            ("Technical University of Munich", "Germany", "Munich"),
            ("LMU Munich", "Germany", "Munich"),
            ("Heidelberg University", "Germany", "Heidelberg"),
            ("RWTH Aachen University", "Germany", "Aachen"),
            ("Humboldt University of Berlin", "Germany", "Berlin"),
            ("University of Hamburg", "Germany", "Hamburg"),
            ("Technical University of Berlin", "Germany", "Berlin"),
            # Hungary
            ("Eötvös Loránd University", "Hungary", "Budapest"),
            ("University of Szeged", "Hungary", "Szeged"),
            ("University of Debrecen", "Hungary", "Debrecen"),
            ("Budapest University of Technology and Economics", "Hungary", "Budapest"),
            ("University of Pécs", "Hungary", "Pécs"),
            # Poland
            ("University of Warsaw", "Poland", "Warsaw"),
            ("Jagiellonian University", "Poland", "Krakow"),
            ("Warsaw University of Technology", "Poland", "Warsaw"),
            ("Adam Mickiewicz University", "Poland", "Poznan"),
            ("University of Wroclaw", "Poland", "Wroclaw"),
            # Czechia
            ("Charles University", "Czechia", "Prague"),
            ("Czech Technical University", "Czechia", "Prague"),
            ("Masaryk University", "Czechia", "Brno"),
            ("Brno University of Technology", "Czechia", "Brno"),
            ("Palacký University", "Czechia", "Olomouc"),
            ("Technical University of Ostrava", "Czechia", "Ostrava")
        ]

        majors_list = [
            "Computer Science", "Data Science", "Artificial Intelligence",
            "Mechanical Engineering", "Civil Engineering", "Electrical Engineering",
            "Business Administration", "Economics", "International Relations",
            "Architecture", "Medicine", "Psychology", "Design"
        ]
        
        deadlines_list = ["2026-05-15", "2026-06-01", "2026-07-15", "2026-08-01"]

        print(f"🚀 Генерация {len(REAL_UNIS)} реальных университетов...")
        all_programs = []

        for uni_name, country, city in REAL_UNIS:
            # Уинверситеттің атынан автоматты түрде ресми сайттың сілтемесін құрастыру
            website_domain = uni_name.split()[0].lower().replace("ö", "o")
            
            uni = models.University(
                name=uni_name,
                country=country,
                city=city,
                description=f"Top-tier educational institution in {country}. Located in the beautiful city of {city}, known for its excellent research and international community.",
                website=f"https://www.{website_domain}.edu"
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
        print(f"✅ Успешно! Создано {len(REAL_UNIS)} университетов и {len(all_programs)} программ.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()