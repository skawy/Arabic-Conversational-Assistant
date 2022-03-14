from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
import sqlite3



class ValidateUserDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

    def validate_phone(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone` value."""

        phone_pattern = re.compile(r"^01[0-2,5]{1}[0-9]{8}$")

        if re.fullmatch(phone_pattern, slot_value):
            dispatcher.utter_message(text=f"'{slot_value}'")
            # add phone number to order_list to save it in database
            order_list.append(slot_value)
            return {"phone": slot_value}
        else:
            dispatcher.utter_message(text=f"'{slot_value}' .الرقم غير صحيح يا فندم ")
            return {"phone": None}

    def validate_id(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `id` value, send the bill to user and insert all values to database"""
        order_list.append(slot_value)
        # order_list[0][0] ==> pizza, order_list[0][1] ==> amount
        # order_list[2] ==> name, order_list[1] ==> phone, order_list[3] ==> id
        done = insert_booking(order_list[0][0], order_list[0][1], order_list[2], order_list[3], order_list[1])
        print(print_booking())
        dispatcher.utter_message(text=done)
        for i in bill:
            dispatcher.utter_message(text=i)
        return {"id": slot_value}

    def validate_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""
        if slot_value == " ":
            dispatcher.utter_message(text=f"الاسم غير صحيح يا فندم.")
            return {"name": None}
        # add name to order_list to save it in database
        order_list.append(slot_value)
        dispatcher.utter_message(text=f"أستاذ {slot_value} .")
        return {"name": slot_value}
