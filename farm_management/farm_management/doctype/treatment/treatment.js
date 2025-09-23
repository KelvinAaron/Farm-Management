// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Treatment", {
	refresh(frm) {
        if (frm.is_new()) {
            frm.set_value("treatment_date", frappe.datetime.now_datetime());
            frappe.db.get_single_value("Livestock Account Settings", "treatment_debit_account") .then((r) => {
                frm.set_value("treatment_account", r);
            });
        }
	},
});
