# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Measurement(Document):
	def on_submit(self):
		livestock = frappe.get_doc(
			"Livestock", self.animal_id
		)
		livestock.append("measurements",
			{
				"measurement_id": self.name,   
			},
		)
		livestock.save()
		frappe.msgprint(f"Livestock with id: {livestock.name}, has been updated")