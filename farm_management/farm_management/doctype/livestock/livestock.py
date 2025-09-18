# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class Livestock(Document):
	def before_insert(self):
		self.status = "Active"

		# item = frappe.get_doc(
		# 	{
		# 		"doctype": "Item",
		# 		"item_code": self.registry_number,
		# 		"item_name": self.registry_number,
		# 		"item_group": self.group,
		# 		"valuation_rate": self.value,
		# 		"has_serial_no": 1,
		# 	}
		# )
		# item.insert()
		# frappe.msgprint(f"Item with id: {item.name}, has been created")

		# serial = frappe.get_doc(
		# 	{
		# 		"doctype": "Serial No",
		# 		"item_code": self.registry_number,
		# 		"serial_no": self.registry_number,
		# 	}
		# )
		# serial.insert()

		# bundle = frappe.get_doc(
		# 	{
		# 		"doctype": "Serial and Batch Bundle",
		# 		"item_code": item.name,
		# 		"warehouse": self.warehouse,
		# 		"type_of_transaction": "Inward",
		# 		"entries": [
		# 			{
		# 				"serial_no": serial.name,
		# 				"qty": 1,
		# 				"warehouse": self.warehouse
		# 			}
		# 		],
		# 		"voucher_type": "Stock Entry"
		# 	}
		# )
		# bundle.insert()


		# stock = frappe.get_doc(
		# 	{
		# 		"doctype": "Stock Entry",
		# 		"stock_entry_type": "Material Receipt",
		# 		"items": [
		# 			{
		# 				"t_warehouse": self.warehouse,
		# 				"item_code": self.registry_number,
		# 				"qty": 1,
		# 				"use_serial_batch_fields": 0,
		# 				"serial_and_batch_bundle": bundle.name
		# 			}
		# 		],
		# 	}
		# )
		# stock.insert().submit()
		# frappe.msgprint(f"Stock entry with id: {stock.name}, has been created")

	def before_save(self):
		if self.treatments:
			total_treatment_cost = 0
			for treatment in self.treatments:
				treatment_total = treatment.cost
				total_treatment_cost += treatment_total
			self.total_treatment_cost = total_treatment_cost

		if self.feedings:
			total_feeding_cost = 0
			for feeding in self.feedings:
				feeding_total = feeding.cost
				total_feeding_cost += feeding_total
			self.total_feeding_cost = total_feeding_cost
				

	@frappe.whitelist()
	def sold(self, reason, debit_to=None, customer=None, income_account=None):
		# Always create the livestock record
		stock_take = frappe.get_doc({
			"doctype": "Livestock Record",
			"date_of_action": frappe.utils.now(),
			"livestock_id": self.name,
			"activity": reason,
		})

		stock_take.insert().submit()
		# frappe.msgprint(f"Livestock Record with id: {stock_take.name}, has been created")

		# Only create Sales Invoice if reason is "Sold"
		if reason == "Sold":
			if not (debit_to and customer and income_account):
				frappe.throw("To mark livestock as Sold, you must provide debit_to, customer, and income_account")

			recon = frappe.get_doc(
				{
					"doctype": "Sales Invoice",
					"customer": customer,
					"due_date": frappe.utils.now(),
					"debit_to": debit_to,
					"items": [
						{
							"item_name": self.registry_number,
							"qty": 1,
							"rate": self.value,
							"uom": "Unit",
							"conversion_factor": 1,
							"income_account": income_account,
						}
					],
				}
			)
			recon.insert().submit()
			frappe.msgprint(f"Sales Invoice with id: {recon.name}, has been created")

		return