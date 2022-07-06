from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.schedule_handling import ask_for_one_subject, get_failed_subjects, gpa_dict, db
from rasa_sdk.events import (SlotSet,ConversationPaused)



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
        
        # tracker.slots.clear()
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
                # tracker.slots.clear()
                dispatcher.utter_message(message)
                return {"id": slot_value}

            # if student ask about schedule
            best_schedule = get_failed_subjects(student_grades, year, gpa)
            dispatcher.utter_message(best_schedule)
            return {"id": slot_value}

        else:
            dispatcher.utter_message('معذرة هذا الid غير صحيح')
            return {"id": None}


class check_chitchat(Action):
    def name(self) -> Text:
        return "action_check_chitchat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        """ it is the function which execute action_check_chitchat """
        
        chitchat_count = tracker.get_slot('chitchat_count')
        if chitchat_count is None:
            chitchat_count = 0.0
        chitchat_count += 1.0 
        print("Out of context count: ", chitchat_count)
        
        if chitchat_count >= 3.0:
            dispatcher.utter_message('لقد خرجت عن سياق المحادثة اكثر من مرة لن يتم الرد علي رسائلك الأن.')
            return [ConversationPaused()]
        
        return [SlotSet("chitchat_count", chitchat_count)]
