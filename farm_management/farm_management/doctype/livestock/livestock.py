# Copyright (c) 2025, Group 2 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class Livestock(Document):
	def before_insert(self):
		self.status = "Active"
		self.date_of_acquire = frappe.utils.now()
		settings = frappe.get_doc("Livestock Account Settings")

		animal_group = frappe.get_doc("Livestock Group", self.animal_group)
		animal_group.number_of_animals += 1
		animal_group.save()

		journal_entry = frappe.get_doc(
			{
				"doctype": "Journal Entry",
				"posting_date": frappe.utils.now(),
				"voucher_type": "Journal Entry",
				"accounts": [
					{
						"account": settings.debit_account,
						"debit_in_account_currency": self.value,
					},
					{
						"account": settings.credit_account,
						"credit_in_account_currency": self.value,
					},
				],
			}
		)
		journal_entry.insert().submit()

	def before_save(self):
		if self.treatments:
			total_treatment_cost = 0
			for treatment in self.treatments:
				treatment_total = treatment.cost
				total_treatment_cost += treatment_total
			self.total_treatment_cost = total_treatment_cost
			self.total_treatment = self.total_treatment_cost

		if self.feedings:
			total_feeding_cost = 0
			for feeding in self.feedings:
				feeding_total = feeding.cost
				total_feeding_cost += feeding_total
			self.total_feeding_cost = total_feeding_cost
			self.total_feeding = self.total_feeding_cost

		
		if self.total_treatment or self.total_feeding:
			self.closing_valuation_rate = self.value + self.total_treatment_cost + self.total_feeding_cost
				

	@frappe.whitelist()
	def sold(self, reason, debit_to=None, customer=None, income_account=None):
		# Always create the livestock record
		stock_take = frappe.get_doc({
			"doctype": "Livestock Record Audit",
			"date_of_action": frappe.utils.now(),
			"livestock_id": self.name,
			"activity": reason,
		})
		stock_take.insert().submit()

		animal_group = frappe.get_doc("Livestock Group", self.animal_group)
		animal_group.number_of_animals -= 1
		animal_group.save()

		settings = frappe.get_doc("Livestock Account Settings")

		journal_entry = frappe.get_doc(
			{
				"doctype": "Journal Entry",
				"posting_date": frappe.utils.now(),
				"voucher_type": "Journal Entry",
				"accounts": [
					{
						"account": settings.debit_account,
						"debit_in_account_currency": 0,
						"credit_in_account_currency": self.closing_valuation_rate,
					},
					{
						"account": settings.credit_account,
						"credit_in_account_currency": 0,
						"debit_in_account_currency": self.closing_valuation_rate,
					},
				],
			}
		)
		journal_entry.insert().submit()
		

	
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
							"rate": self.closing_valuation_rate,
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