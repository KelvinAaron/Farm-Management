// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
	refresh(frm) {
        frm.toggle_enable("breed", frm.doc.animal_type);
	},
    animal_type(frm) {
        frm.toggle_enable("breed", frm.doc.animal_type);
        frm.set_query("breed", () => {
            return {
                filters: {
                    "animal_type": frm.doc.animal_type
                }
            }
        })

        if (frm.doc.breed) {
            frm.set_value("breed", "")
        }
    }
});
