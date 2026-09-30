"""
UniMentor AI - Sample Document Generator
========================================
Creates the documents/ folder structure and writes the three
sample university documents into it.

Run once from the project root:
    py setup_documents.py
"""

import os

BASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "documents",
)

CURRICULUM = """UNIVERSITY ACADEMIC REGULATIONS - B.TECH COMPUTER SCIENCE AND ENGINEERING

1. PROGRAMME STRUCTURE
The B.Tech programme is of four years duration, divided into eight semesters.
A student must earn a total of 160 credits to be awarded the degree.
The credit distribution is as follows:
- Core Engineering Courses: 92 credits
- Professional Electives: 18 credits
- Open Electives: 12 credits
- Laboratory and Practical Courses: 22 credits
- Project Work and Internship: 16 credits

2. CREDIT SYSTEM
One lecture hour per week is equal to one credit.
One tutorial hour per week is equal to one credit.
Two laboratory hours per week are equal to one credit.

3. ATTENDANCE REQUIREMENT
A student must maintain a minimum of 75 percent attendance in every
registered course to be permitted to appear in the end semester examination.
A student with attendance between 65 and 75 percent may apply to the Dean
for condonation with valid medical documents. Attendance below 65 percent
carries no provision for condonation and the student must repeat the course.

4. EVALUATION AND GRADING
Internal assessment carries 50 marks and the end semester examination
carries 50 marks. The internal assessment is divided into Mid Semester
Examination (30 marks), Quizzes (10 marks) and Assignments (10 marks).

Letter grades and grade points:
O = 10 points, marks 90 and above
E = 9 points, marks 80 to 89
A = 8 points, marks 70 to 79
B = 7 points, marks 60 to 69
C = 6 points, marks 50 to 59
D = 5 points, marks 40 to 49
F = 0 points, marks below 40 (Fail)

A student must score a minimum of 40 percent in aggregate and a minimum of
30 percent in the end semester examination to pass a course.

5. BACKLOG AND RE-EXAMINATION
A student who fails a course is permitted to appear in the supplementary
examination held at the end of the following semester. A maximum of four
attempts is permitted per course. A student carrying more than six backlogs
at the end of the fourth semester is not permitted to register for
seventh semester courses.

6. PROFESSIONAL ELECTIVES FOR CSE
Professional electives are offered from the fifth semester onwards.
Each professional elective carries 3 credits. A student must complete six
professional electives in total.
Available electives include:
- CS3001 Machine Learning
- CS3002 Cloud Computing
- CS3003 Cyber Security
- CS3004 Data Mining and Data Warehousing
- CS3005 Internet of Things
- CS3006 Natural Language Processing
- CS3007 Blockchain Technology
- CS3008 Computer Vision

7. PROJECT WORK
The Minor Project is undertaken in the sixth semester and carries 4 credits.
The Major Project is undertaken across the seventh and eighth semesters and
carries 8 credits. The Summer Internship after the sixth semester carries
4 credits and requires a minimum duration of six weeks.

8. CGPA CALCULATION
CGPA is the weighted average of grade points across all completed semesters,
weighted by the credits of each course. The percentage equivalent of CGPA
is obtained by multiplying the CGPA by 9.5.
"""

PLACEMENT = """UNIVERSITY TRAINING AND PLACEMENT POLICY

1. REGISTRATION
All students seeking placement assistance must register with the Training
and Placement Cell at the beginning of the seventh semester. Registration
requires a verified resume, updated academic record and a passport size
photograph. Students who do not register by the notified date will not be
considered for any campus drive during that academic year.

2. ELIGIBILITY CRITERIA
The general eligibility criteria for participation in campus placement are:
- Minimum CGPA of 7.0 up to the sixth semester
- No active backlog at the time of the company drive
- Not more than one year of academic gap in the entire education history
- Minimum 75 percent aggregate in Class 10 and Class 12

Individual companies may set higher criteria than the general criteria.
Company specific criteria always override the general criteria.

3. ONE STUDENT ONE OFFER POLICY
A student who accepts an offer is removed from further placement drives.
A placed student may appear for a further company only if the new offer
has an annual package at least twice the value of the existing offer and
the existing offer is below 8 lakh per annum. Prior written approval from
the Placement Officer is mandatory in such cases.

4. CATEGORISATION OF COMPANIES
Companies are categorised by annual package:
- Super Dream: above 20 lakh per annum
- Dream: 10 to 20 lakh per annum
- Core: 6 to 10 lakh per annum
- Mass Recruiter: below 6 lakh per annum

A student placed in a Mass Recruiter company remains eligible for Dream
and Super Dream companies. A student placed in a Dream company remains
eligible only for Super Dream companies.

5. ATTENDANCE IN THE RECRUITMENT PROCESS
Once a student applies to a company, attending every round of that
company's process is compulsory. A student who withdraws after applying,
or who is absent from any round without written permission, is debarred
from the next two company drives.

6. INTERNSHIP POLICY
Six month internships are permitted in the eighth semester provided the
student has no pending backlog and the organisation submits an official
offer letter to the Placement Cell. The internship must be approved by the
Head of Department. A student on a six month internship must submit a
fortnightly progress report to the assigned faculty mentor.

7. PREPARATION SUPPORT
The Placement Cell conducts aptitude training from the fifth semester,
technical mock interviews from the sixth semester and communication skills
workshops throughout the seventh semester. Attendance in placement training
sessions is tracked and a minimum of 80 percent attendance in training is
required to remain eligible for Super Dream company drives.

8. CODE OF CONDUCT
Misrepresentation of marks, CGPA, project work or internship experience in
a resume results in permanent debarment from campus placement and is
reported to the Disciplinary Committee.
"""

SCHOLARSHIP = """UNIVERSITY SCHOLARSHIP AND FINANCIAL AID GUIDELINES

1. MERIT SCHOLARSHIP
The Merit Scholarship is awarded to students who achieve a CGPA of 9.0 or
above in the preceding academic year. The scholarship covers 50 percent of
the tuition fee for the following academic year. The number of awards is
limited to the top 5 percent of students in each branch.
Application deadline: 31 August every year.
Required documents: semester grade cards, fee receipt, Aadhaar copy and a
bank account passbook copy.

2. MEANS CUM MERIT SCHOLARSHIP
Students with a family income below 4 lakh per annum and a CGPA of 8.0 or
above are eligible. The scholarship covers 30 percent of the tuition fee.
Application deadline: 30 September every year.
Required documents: income certificate issued by a competent authority
within the last six months, grade cards, fee receipt and bank details.

3. SPORTS AND CULTURAL SCHOLARSHIP
Students who have represented the state or the country in a recognised
sport or cultural competition are eligible for a scholarship covering
25 percent of the tuition fee. A minimum CGPA of 6.5 must be maintained.
Application deadline: 15 October every year.
Required documents: participation and achievement certificates attested by
the relevant federation, and the latest grade card.

4. FIRST GENERATION LEARNER SUPPORT
Students who are the first in their family to attend university and whose
family income is below 3 lakh per annum may apply for a fee waiver of up to
40 percent. A declaration signed by a parent or guardian is required along
with an income certificate.
Application deadline: 30 September every year.

5. RENEWAL CONDITIONS
All scholarships are granted for one academic year and must be renewed.
Renewal requires that the student maintains the CGPA threshold of the
original scholarship, has no disciplinary action recorded during the year,
and maintains a minimum of 75 percent attendance. A student who fails any
course during the year becomes ineligible for renewal for that year.

6. DISBURSEMENT
Approved scholarship amounts are adjusted against the tuition fee of the
following semester. Scholarships are not disbursed in cash. Where the fee
has already been paid in full, the amount is refunded to the registered
bank account within 45 working days of approval.

7. MULTIPLE SCHOLARSHIPS
A student may hold only one university scholarship at a time. Where a
student qualifies for more than one, the scholarship with the higher
benefit is awarded. University scholarships may be held alongside
government scholarships unless the government scheme prohibits it.

8. APPLICATION PROCEDURE
Applications are submitted through the student portal under the Financial
Aid section. Incomplete applications and applications received after the
deadline are rejected without exception. The Scholarship Committee
publishes results within 30 days of the deadline.
"""

FILES = {
    ("curriculum", "academic_regulations.txt"): CURRICULUM,
    ("placement", "placement_policy.txt"): PLACEMENT,
    ("scholarship", "scholarship_guidelines.txt"): SCHOLARSHIP,
}


def main():
    for (department, filename), content in FILES.items():
        folder = os.path.join(BASE, department)
        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, filename)

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Created: {path}")

    print("\nDone. Now run:  py -m streamlit run app.py")


if __name__ == "__main__":
    main()