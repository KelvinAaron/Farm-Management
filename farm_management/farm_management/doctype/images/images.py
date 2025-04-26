# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Images(Document):
	def after_insert(self):
		livestock = frappe.get_doc("Livestock", self.animal_id)

		livestock.append("images", { 
			"image_id": self.name,  
			"image": self.image, 
		})
		livestock.save()
		frappe.msgprint(f"Livestock with id: {livestock.name}, has been updated")