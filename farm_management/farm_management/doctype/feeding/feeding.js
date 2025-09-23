// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Feeding", {
	refresh(frm) {
        if (frm.is_new()) {
            frm.set_value("feeding_date", frappe.datetime.now_datetime());
            frappe.db.get_single_value("Livestock Account Settings", "feedings_debit_account") .then((r) => {
                frm.set_value("feeding_account", r);
            });
        }
	},
});
