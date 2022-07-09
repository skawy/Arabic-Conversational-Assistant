from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.schedule_handling import ask_for_one_subject, get_failed_subjects, gpa_dict, db, get_schedule
from rasa_sdk.events import (SlotSet, ConversationPaused)


class schedule_maker(Action):
    def name(self) -> Text:
        return "action_get_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        student_id = tracker.get_slot('id')
        if student_id is None:
            print ("فاضية يا ")

        student_information = gpa_dict[student_id]
        print("id gadwall:", student_id)
        gpa = student_information[1]
        year = student_information[-1] + student_information[-2]
        print("year",year)
        student_grades, subjects_list = db.get_tables(student_id)

        subject = tracker.get_slot('subject')
        if subject is not None:
            message = ask_for_one_subject(subject, student_grades, subjects_list)
            dispatcher.utter_message(message)
            # dispatcher.utter_message(response = "action_check_subject_name")
            return [SlotSet("subject",None)]

        if student_id is not None:
            if 'f' in student_grades.keys():
                failed_subject = student_grades['f']
                best_schedule = get_failed_subjects(failed_subject, year, gpa)
                dispatcher.utter_message(best_schedule)

            else :
                dispatcher.utter_message(get_schedule(year))
            
            return[]

        dispatcher.utter_message('الid لو سمحت')
        return []
   


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
        id = tracker.get_slot('id')
        print(id)
        if id is not None:
            student_grades, subjects = db.get_tables(id)
            message = ask_for_one_subject(subject, student_grades, subjects)
            dispatcher.utter_message(message)
            return [SlotSet("subject",None)]

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
                SlotSet("id", slot_value)
            except KeyError:
                # if id not is database
                dispatcher.utter_message('الid دا مش متسجل ابعته تانى لو سمحت')
                return {"id": None}

            # get student information gpa, year and grades
            # dispatcher.utter_message(response = "action_get_schedule")
            # dispatcher.utter_message(response = "action_check_subject_name")
            # dispatcher.utter_message(";glm uh]d")
            
            # subject_name = tracker.get_slot('subject')
            # if subject_name is not None:
            #     # if student ask for specific subject
            #     # message = ask_for_one_subject(subject_name, student_grades, subjects)
            #     dispatcher.utter_message(response = "action_check_subject_name")
            #     # return {"id": slot_value}

            # if subject_name is None:
            #     print("اي كلام")
            #     dispatcher.utter_message(response = "action_get_schedule")
            
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
