from agent import run_agent


def collect_student_info() -> dict:
    print("=" * 62)
    print("        OPPORTUNITY SCOUT — African Student Opportunities")
    print("=" * 62)
    print("I'll search the web for internships, fellowships, and grants")
    print("tailored specifically to your profile.\n")

    def prompt(label: str, hint: str = "") -> str:
        display = f"{label}" + (f" ({hint})" if hint else "") + ": "
        while True:
            value = input(display).strip()
            if value:
                return value
            print(f"  ⚠  {label} cannot be empty. Please try again.")

    name = prompt("Your Name")
    field_of_study = prompt("Field of Study", "e.g. Computer Science, Medicine, Engineering")
    skills = prompt("Your Skills", "e.g. Python, data analysis, research, leadership")
    year_of_study = prompt("Year of Study", "e.g. 2nd year, Final year, Postgraduate")

    return {
        "name": name,
        "field_of_study": field_of_study,
        "skills": skills,
        "year_of_study": year_of_study,
    }


def main():
    student_info = collect_student_info()

    print(f"\nGreat! Searching for opportunities for {student_info['name']}...")

    result = run_agent(student_info)

    print("\n" + "=" * 62)
    print("                    OPPORTUNITIES FOUND")
    print("=" * 62 + "\n")
    print(result)
    print("\n" + "=" * 62)
    print("  Good luck with your applications!  — Opportunity Scout")
    print("=" * 62)


if __name__ == "__main__":
    main()
