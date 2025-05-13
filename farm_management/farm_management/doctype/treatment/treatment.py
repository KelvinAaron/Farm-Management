# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Treatment(Document):
    def on_submit(self):
        # Gets the available quantity for product in warehouse, and
        # makes sure treatment quantity is not greater.
        item_bin = frappe.db.get_value(
            "Bin",
            {
                "item_code": self.product_details,
                "warehouse": self.warehouse,
            },
            ["name", "actual_qty"],
            as_dict=True
        )
        if item_bin.actual_qty < self.quantity:
            frappe.throw(f"Max quantity: {item_bin.actual_qty}")

        stock = frappe.get_doc(
            {
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Issue",
                "items": [
                    {
                        "s_warehouse": self.warehouse,
                        "item_code": self.product_details,
                        "qty": self.quantity,
                    }
                ],
            }
        )
        stock.insert().submit()
        frappe.msgprint(f"Stock entry with id: {stock.name}, has been created")

        livestock = frappe.get_doc("Livestock", self.animal_id)
        livestock.append(
            "treatments",
            {
                "treatment_id": self.name,
            },
        )

        livestock.save()
        frappe.msgprint(f"Livestock with id: {livestock.name}, has been updated")
