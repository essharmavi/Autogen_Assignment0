# Autogen JD & Questionnaire Generator

## Overview
An automated system that:
1. Creates a **Job Description (JD)** from user input.
2. Generates an **interview questionnaire** from the JD.
3. Exports both as **PDFs**.
4. User can jump in to make changes or approving the output by agents.

Built using [Autogen](https://github.com/microsoft/autogen) with **multi-agent collaboration**.

---

## How It Works
- **JD Creation Team** → Generates JD → Saves as PDF.
- **Questionnaire Team** → Reads JD → Generates questionnaire → Saves as PDF.

---


## Run the Project
pip install -r requirements.txt
python main.py

## Output
**JD PDF**: output/JD/jd_output.pdf
**Questionnaire PDF**: output/Questionnaire/questionnaire_output.pdf

## Contact
**Author:** Vishal Sharma
**LinkedIn:** https://www.linkedin.com/in/essharmavi/
