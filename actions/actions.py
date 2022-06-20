from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.FCAI_DB import FCAI_DB

# Access database
db = FCAI_DB()
""" if FCAI Subjects.dp is deleted uncomment below line """
# db.create_DB()
bylaw = db.get_tables('bylaw')
gpa_dict = db.get_tables('GPA')
schedule = db.get_schedule()


def get_subjects_priority(student_schedule, gpa):
    """
        Parameters:
            student_schedule: list of semester subject's
            gpa: int of student's GPA

        Return:
            student_schedule: string of best schedule
    """

    min_priority = {}

    for i in student_schedule:
        if i not in bylaw.keys():
            # if subject not in bylaw give it 0 priority
            min_priority[i] = 0
        else:
            min_priority[i] = int(bylaw[i][-1])
    # sort priorities ascending
    min_priority = sorted(min_priority.items(), key=lambda x: x[1], reverse=False)

    try:
        """ check on gpa to know how many subjects can be registered by student """
        if 1.5 < gpa < 2:
            student_schedule.remove(min_priority[0][0])
            student_schedule.remove(min_priority[1][0])

        elif gpa < 1.5:
            student_schedule.remove(min_priority[0][0])
            student_schedule.remove(min_priority[1][0])
            student_schedule.remove(min_priority[2][0])

        return ', '.join(student_schedule)
    except (KeyError, ValueError):
        print(KeyError, ValueError)


def get_best_schedule(student_schedule, failed_subject, gpa):
    """
        Searching on which subject in the schedule is depended on the failed subjects
                change the failed subjects with subject which depend on it

        Parameters:
            student_schedule: list of semester subjects
            failed_subject: list of failed subjects
            gpa: int of student GPA

        Return:
            best_schedule: string of best schedule
    """

    for i in student_schedule:
        index = student_schedule.index(i)
        # if subject is in bylaw
        if i in bylaw.keys():
            # check on this subject has 2 or 1 perquisite
            if len(bylaw[i]) > 1:
                if bylaw[i][0] in failed_subject:
                    student_schedule[index] = bylaw[0]

                elif bylaw[i][1] in failed_subject:
                    student_schedule[index] = bylaw[i][1]

            else:
                if bylaw[i][0] in failed_subject:
                    student_schedule[index] = bylaw[i][0]

    best_schedule = get_subjects_priority(student_schedule, int(gpa))
    return best_schedule


def get_failed_subjects(student_grades, year, gpa):
    """
        Parameters:
            student_grades: dictionary of student's results
            year: string of student's year and his department
            gpa: string of GPA

        Return:
            best_schedule: string of best schedule
    """

    if 'f' not in student_grades.keys():
        return 'سجل الجدول الطبيعى'

    # get schedule of his year
    student_schedule = schedule[year]
    # get failed subjects
    failed_subject = student_grades['f']
    best_schedule = get_best_schedule(student_schedule, failed_subject, gpa)
    return best_schedule


class ValidateUserDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_student_id_form"

    def validate_id(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `id` value"""
        id_pattern = re.compile(r"^20[0-9]{2}[0-2][0-9]{3}$")

        if re.fullmatch(id_pattern, slot_value):
            student_information = gpa_dict[slot_value]

            if len(student_information) == 0:
                dispatcher.utter_message('مفيش الid دا')
                return {"id": None}

            gpa = student_information[1]
            year = student_information[-1] + student_information[-2]
            student_grades = db.get_tables(slot_value)
            best_schedule = get_failed_subjects(student_grades, year, gpa)
            dispatcher.utter_message(best_schedule)
            return {"id": slot_value}
        else:
            dispatcher.utter_message('معذرة هذا الid غير صحيح')
            return {"id": None}
