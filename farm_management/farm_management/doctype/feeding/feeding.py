# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Feeding(Document):
	def before_save(self):
		self.total_cost = self.quantity * self.valuation_rate

	def on_submit(self):
		total_quantity = self.quantity

		if self.entry_type == "Group":
			animal_group = frappe.get_doc("Livestock Group", self.group_id)
			quantity = animal_group.number_of_animals
			total_quantity = self.quantity * quantity
		
		stock = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Issue",
				"items": [
					{
						"s_warehouse": self.warehouse,
                        "item_code": self.product,
                        "qty": total_quantity,
					}
				]				
			}
		)
		stock.insert().submit()
		frappe.msgprint(f"Stock entry with id: {stock.name}, has been created")

		if self.entry_type == "Group":
			livestock_list = frappe.get_all(
                "Livestock",
                filters={"animal_group": self.group_id, "status": "Active"},
            )

			for livestock in livestock_list:
				livestock_doc = frappe.get_doc("Livestock", livestock.name)
				livestock_doc.append("feedings",
                    {
                        "feeding_id": self.name,
                    },
                )
				livestock_doc.save()
			frappe.msgprint(f"Livestocks in group with id: {self.group_id}, has been updated")

		elif self.entry_type == "Individual":
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