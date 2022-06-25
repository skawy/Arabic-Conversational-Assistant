from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.schedule_handling import ask_for_one_subject, get_failed_subjects, gpa_dict, db


class check_subject_name(Action):
    def name(self) -> Text:
        return "action_check_subject_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ it is the function which execute action_check_subject_name """
        subject = tracker.get_slot('subject')
        print(subject)
        if subject is None:
            dispatcher.utter_message('بعد أذنك دخل أسم المادة بالأنجليزى')
            return []
        
        tracker.slots.clear()
        print(tracker.get_slot('subject'))
        dispatcher.utter_message('الid لو سمحت')
        return []


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
            try:
                student_information = gpa_dict[slot_value]
            except KeyError:
                # if id not is database
                dispatcher.utter_message('الid دا مش متسجل ابعته تانى لو سمحت')
                return {"id": None}

            # get student information gpa, year and grades
            subject_name = tracker.get_slot('subject')
            gpa = student_information[1]
            year = student_information[-1] + student_information[-2]
            student_grades = db.get_tables(slot_value)

            if subject_name is not None:
                # if student ask for specific subject
                message = ask_for_one_subject(subject_name, student_grades)
                tracker.slots.clear()
                dispatcher.utter_message(message)
                return {"id": slot_value}

            # if student ask about schedule
            best_schedule = get_failed_subjects(student_grades, year, gpa)
            dispatcher.utter_message(best_schedule)
            return {"id": slot_value}

        else:
            dispatcher.utter_message('معذرة هذا الid غير صحيح')
            return {"id": None}
