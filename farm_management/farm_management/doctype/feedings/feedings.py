# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Feedings(Document):
	def after_insert(self):
		stock = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Issue",
				"items": [
					{
						"s_warehouse": "Finished Goods - E",
                        "item_code": self.product,
                        "qty": self.quantity,
					}
				]
			}
		)
		stock.insert()
		frappe.msgprint(f"Stock with id: {stock.name}, has been created")