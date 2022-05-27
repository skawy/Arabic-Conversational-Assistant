from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
from actions.FCAI_DB import FCAI_DB as db


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
        phone_pattern = re.compile(r"^20[0-9]{2}[0-2][0-9]{3}$")
        print(phone_pattern)
        if re.fullmatch(phone_pattern, slot_value):
            dispatcher.utter_message('id')
            return {"id": slot_value}
        else:
            dispatcher.utter_message('معذرة لا يوجد هذا الid')
            return {"id": None}

