from cgitb import text
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.schedule_handling import ask_for_one_subject, get_failed_subjects, gpa_dict, db, get_schedule
from rasa_sdk.events import (SlotSet, FollowupAction, ConversationPaused, ConversationResumed)
from datetime import datetime


class schedule_maker(Action):
    def name(self) -> Text:
        return "action_get_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        student_id = tracker.get_slot('id')

        if student_id is not None:
            if student_id not in gpa_dict.keys():
                dispatcher.utter_message(text="معذرة هذا الid غير متسجل \n")
                return [SlotSet('id', None)]

            else:
                student_information = gpa_dict[student_id]
                gpa = student_information[0]
                year = student_information[-1] + student_information[-2]
                student_grades, subjects_list, cumulative_hours = db.get_tables(student_id)

                subject = tracker.get_slot('subject')
                if subject is not None:
                    message = ask_for_one_subject(subject, student_grades, subjects_list, cumulative_hours)
                    dispatcher.utter_message(message)
                    return [SlotSet("subject", None)]

                if 'f' in student_grades.keys():
                    failed_subject = student_grades['f']
                    best_schedule = get_failed_subjects(failed_subject, year, gpa)
                    dispatcher.utter_message(best_schedule)

                else:
                    dispatcher.utter_message(get_schedule(year))

                return []

        dispatcher.utter_message(response="utter_ask_for_id")
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

        id = tracker.get_slot('id')

        if id is not None:
            student_grades, subjects, cumulative_hours = db.get_tables(id)
            message = ask_for_one_subject(subject, student_grades, subjects, cumulative_hours)
            dispatcher.utter_message(message)
            return [SlotSet("subject", None)]

        dispatcher.utter_message(response="utter_ask_for_id")
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
        id_pattern = re.compile("^20[0-2]{1}\d{1}[0-2]{1}\d{3}$")
        print(slot_value)

        if re.fullmatch(id_pattern, slot_value):
            return {"id": slot_value}
        else:
            dispatcher.utter_message(response="utter_wrong_id")
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
        # print("Out of context count: ", chitchat_count)

        if chitchat_count >= 3.0:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f' Pausing Conversation {tracker.sender_id} in Time {current_time}')

            with open("./paused_ids.txt", 'a') as file1:
                file1.write(f'{tracker.sender_id}\n')

            chitchat_count = 0.0

            return [SlotSet("chitchat_count", chitchat_count), ConversationPaused()]

        dispatcher.utter_message(f' دى المره رقم {int(chitchat_count)} الى تخرج فيها عن السياق التزم بالمحادثه بعد '
                                 f'اذنك حتى لايتم غلق المحادثه')

        if chitchat_count == 2.0:
            dispatcher.utter_message('لو خرجت بره السياق تانى المحادثه هتتقفل كحد أقصى لمدة خمس ساعات')

        return [SlotSet("chitchat_count", chitchat_count)]


class Ask_for_courses(Action):
    def name(self) -> Text:
        return "action_asking_for_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ it is the function which execute action_check_chitchat """

        grade = tracker.get_slot('grade')

        if grade is not None:
            dispatcher.utter_message(text="تقدر تشوف الbylaw من موقع الكلية فيها تفاصيل كل المواد")
            return []

# class Training(Action):
#     def name(self) -> Text:
#         return "action_training_respond"

#     @staticmethod
#     def calculate_hours_for_training(student_id):
#         _, _, cumulative_hours = db.get_tables(student_id)
#         link = 'https://github.com/ACM-Alexandria-SC/Internships'
#         if cumulative_hours >= 45:
#             return f'انت اجتزت 45 ساعة و تقدر تسجل التدريب و دا لينك لشركات {link}'
#         else:
#             return 'للأسف لازم تجتاز 45 ساعة و انت لسه معدتهمش'

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         """ it is the function which execute action_check_chitchat """

#         student_id = tracker.get_slot('id')
#         if student_id is not None:
#             dispatcher.utter_message(self.calculate_hours_for_training(student_id))
#             return [SlotSet('training', 'Done')]

#         dispatcher.utter_message("لازم تدخل الid بتاعك")
#         return []
