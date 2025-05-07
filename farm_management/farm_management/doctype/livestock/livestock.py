# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Livestock(Document):
	def before_insert(self):
		self.status = "Active"

		item = frappe.get_doc(
			{
				"doctype": "Item",
				"item_code": self.registry_number,
				"item_name": self.registry_number,
				"item_group": self.group,
				"valuation_rate": self.value,
				"has_serial_no": 1,
			}
		)
		item.insert()
		frappe.msgprint(f"Item with id: {item.name}, has been created")

		serial = frappe.get_doc(
			{
				"doctype": "Serial No",
				"item_code": self.registry_number,
				"serial_no": self.registry_number,
			}
		)
		serial.insert()

		bundle = frappe.get_doc(
			{
				"doctype": "Serial and Batch Bundle",
				"item_code": item.name,
				"warehouse": self.warehouse,
				"type_of_transaction": "Inward",
				"entries": [
					{
						"serial_no": serial.name,
						"qty": 1,
						"warehouse": self.warehouse
					}
				],
				"voucher_type": "Stock Entry"
			}
		)
		bundle.insert()


		stock = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Receipt",
				"items": [
					{
						"t_warehouse": self.warehouse,
						"item_code": self.registry_number,
						"qty": 1,
						"use_serial_batch_fields": 0,
						"serial_and_batch_bundle": bundle.name
					}
				],
			}
		)
		stock.insert().submit()
		frappe.msgprint(f"Stock entry with id: {stock.name}, has been created")


	@frappe.whitelist()
	def terminate(self):

		recon = frappe.get_doc(
			{
				"doctype": "Stock Reconciliation",
				"purpose": "Stock Reconciliation",
				"items": [
					{
						"item_code": self.registry_number,
						"warehouse": self.warehouse,
						"qty": 0,
						"use_serial_batch_fields": 1,
					}
				],
			}
		)

		recon.insert().submit()

		message = f"Stock Reconciliation with id: {recon.name}, has been created"
		frappe.msgprint(message)
		return message
		
		
		
		
