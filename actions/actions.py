# actions/actions.py

from typing import Any, Text, Dict, List
from datetime import datetime
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionAddToCart(Action):

    def name(self) -> Text:
        return "action_add_to_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message.get("text", "").lower()

        cart = tracker.get_slot("cart_items") or []
        total = tracker.get_slot("total_amount") or 0

        item_name = ""
        item_price = 0

        if "biryani" in latest_message:
            item_name = "Veg Biryani"
            item_price = 180

        elif "dosa" in latest_message:
            item_name = "Masala Dosa"
            item_price = 110

        elif "thali" in latest_message:
            item_name = "Punjabi Thali"
            item_price = 150

        elif "rice" in latest_message:
            item_name = "Fried Rice"
            item_price = 140

        elif "noodles" in latest_message:
            item_name = "Veg Noodles"
            item_price = 130

        elif "lassi" in latest_message:
            item_name = "Mango Lassi"
            item_price = 90

        if item_name:

            cart.append({
                "name": item_name,
                "price": item_price
            })

            total += item_price

            dispatcher.utter_message(
                text=f"""✅ Added to Cart!

1 x {item_name}
Price: ₹{item_price}

Click "View Cart" to review!"""
            )

        else:

            dispatcher.utter_message(
                text="❌ Item not found in menu."
            )

        return [
            SlotSet("cart_items", cart),
            SlotSet("total_amount", total)
        ]


class ActionShowCart(Action):

    def name(self) -> Text:
        return "action_show_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cart = tracker.get_slot("cart_items") or []
        total = tracker.get_slot("total_amount") or 0

        if not cart:

            dispatcher.utter_message(
                text="🛒 Your cart is empty."
            )

            return []

        cart_text = "🛒 Your Cart\n\n"

        for item in cart:
            cart_text += f"• {item['name']} = ₹{item['price']}\n"

        cart_text += f"\n────────────\n\n💜 Total: ₹{total}"
        cart_text += "\n\nClick \"Confirm\" to place order!"

        dispatcher.utter_message(text=cart_text)

        return []


class ActionClearCart(Action):

    def name(self) -> Text:
        return "action_clear_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="🗑️ Cart cleared!"
        )

        return [
            SlotSet("cart_items", []),
            SlotSet("total_amount", 0)
        ]


class ActionConfirmOrder(Action):

    def name(self) -> Text:
        return "action_confirm_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cart = tracker.get_slot("cart_items") or []
        total = tracker.get_slot("total_amount") or 0

        if not cart:

            dispatcher.utter_message(
                text="🛒 Your cart is empty."
            )

            return []

        order_history = tracker.get_slot("order_history") or []

        order_id = f"ORD{random.randint(1000000000,9999999999)}"

        order_data = {
            "order_id": order_id,
            "items": cart.copy(),
            "total": total,
            "date": datetime.now().strftime("%d/%m/%Y %I:%M %p")
        }

        order_history.append(order_data)

        dispatcher.utter_message(
            text=f"""✅ Order Confirmed!

Order ID: {order_id}

Total: ₹{total}

🎉 Thank you! Your order will be ready in 30–45 minutes!"""
        )

        return [
            SlotSet("order_history", order_history),
            SlotSet("cart_items", []),
            SlotSet("total_amount", 0)
        ]


class ActionOrderHistory(Action):

    def name(self) -> Text:
        return "action_order_history"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        history = tracker.get_slot("order_history") or []

        if not history:

            dispatcher.utter_message(
                text="📜 No previous orders found."
            )

            return []

        history_text = "📜 Order History\n\n"

        for order in reversed(history):

            history_text += f"{order['order_id']}\n"
            history_text += f"📅 {order['date']}\n"
            history_text += f"📦 {len(order['items'])} item(s)\n"
            history_text += f"Total: ₹{order['total']}\n\n"

        dispatcher.utter_message(text=history_text)

        return []