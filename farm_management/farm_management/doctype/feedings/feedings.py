# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Feedings(Document):
	def before_save(self):
		self.total_cost = self.quantity * self.valuation_rate

	def on_submit(self):
		stock = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Issue",
				"items": [
					{
						"s_warehouse": self.warehouse,
                        "item_code": self.product,
                        "qty": self.quantity,
					}
				]
			}
		)
		stock.insert().submit()
		frappe.msgprint(f"Stock entry with id: {stock.name}, has been created")

		livestock = frappe.get_doc(
			"Livestock", self.animal_id
		)
		livestock.append("feedings",
			{
				"feeding_id": self.name,  
			},
		)
		livestock.save()
		frappe.msgprint(f"Livestock with id: {livestock.name}, has been updated")