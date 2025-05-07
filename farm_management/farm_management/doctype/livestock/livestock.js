// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
    refresh(frm) {
        frm.set_value("group", "Animal")
        frm.toggle_enable("group", false)

        frm.toggle_enable("breed", frm.doc.animal_type);
        if (frm.doc.status == "Active") {
            frm.add_custom_button('Terminate', () => {
                frappe.prompt(
                    {
                        label: 'Reason for Termination',
                        fieldname: 'reason',
                        fieldtype: 'Select',
                        options: ['Sold', 'Dead'],
                        reqd: 1
                    }
                    ,
                    (values) => {
                        console.log(values.reason)
                        frappe.confirm(
                            `Are you sure you want to terminate this livestock for reason: ${values.reason}?`,
                            () => {
                                frm.call("terminate").then(r => {
                                    frm.set_value("status", values.reason)
                                    frm.save()
                                });
                            }
                        )
                    }
                )

            })


        }
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
