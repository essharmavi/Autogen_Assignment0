import fitz  # PyMuPDF, unrelated but OK
from pathlib import Path
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pydantic_model import JobDescription, Questionnaire


def get_jd_pdf(jd: JobDescription):

    current_file = Path(__file__)
    parent_folder = current_file.parent.parent
    output_dir = os.path.join(parent_folder, "output", "JD")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    filename = f"{jd.job_profile.replace(' ', '_')}_JD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = output_dir + "/" + filename

    doc = fitz.open()
    page = doc.new_page()

    print("I am generating pdf")

    text_lines = [
        f"Job Profile: {jd.job_profile}",
        f"Experience: {jd.experience}",
        f"Skills: {', '.join(jd.skills)}",
    ]
    if jd.company_name:
        text_lines.append(f"Company: {jd.company_name}")
    if jd.location:
        text_lines.append(f"Location: {jd.location}")
    if jd.additional_requirements:
        text_lines.append(f"Additional Requirements: {jd.additional_requirements}")

    x, y = 50, 50
    for line in text_lines:
        page.insert_text((x, y), line, fontsize=12)
        y += 20

    doc.save(str(output_path))
    doc.close()
    return "JD PDF generated successfully. TERMINATE!"


def questionnaire_to_pdf(questionnaire: Questionnaire):
    current_file = Path(__file__)
    parent_folder = current_file.parent.parent
    output_dir = os.path.join(parent_folder, "output", "Questionnaire")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{questionnaire.title.replace(' ', '_')}_Questionnaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, filename)

    doc = fitz.open()
    page = doc.new_page()

    title_font_size = 18
    question_font_size = 12
    answer_font_size = 11

    y_position = 50

    page.insert_text(
        (50, y_position),
        questionnaire.title,
        fontsize=title_font_size,
        fontname="helv",
        fill=(0, 0, 0),
    )
    y_position += 40

    for idx, qa in enumerate(questionnaire.questions, start=1):
        question_text = f"Q{idx}. {qa}"
        page.insert_text(
            (50, y_position),
            question_text,
            fontsize=question_font_size,
            fontname="helv",
            fill=(0, 0, 0),
        )
        y_position += 20

        if y_position > page.rect.height - 50:
            page = doc.new_page()
            y_position = 50

    # Save PDF
    doc.save(output_path)
    doc.close()

    return "Questionnaire PDF generated successfully. TERMINATE!"


