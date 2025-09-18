// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
    refresh(frm) {   
        frm.toggle_enable("breed", frm.doc.animal_type);
        if (frm.doc.status == "Active") {
            frm.add_custom_button('Activity', () => {
                frappe.prompt(
                    [
                        {
                            label: 'Reason for Termination',
                            fieldname: 'reason',
                            fieldtype: 'Select',
                            options: ['Sold', 'Dead', 'Missing', 'Slaughtered'],
                            reqd: 1
                        },
                        {
                            label: 'Customer',
                            fieldname: 'customer',
                            fieldtype: 'Link',
                            options: 'Customer', 
                            depends_on: 'eval:doc.reason == "Sold"',
                            mandatory_depends_on: 'eval:doc.reason == "Sold"'
                        },
                        {
                            label: 'Debit To',
                            fieldname: 'debit_to',
                            fieldtype: 'Link',
                            options: 'Account',
                            depends_on: 'eval:doc.reason == "Sold"',
                            mandatory_depends_on: 'eval:doc.reason == "Sold"',
                            get_query: () => {
                                return {
                                    filters: {
                                        account_type: 'Receivable', 
                                        is_group: 0              
                                    }
                                }
                            }
                        },
                        {
                            label: 'Income Account',
                            fieldname: 'income_account',
                            fieldtype: 'Link',
                            options: 'Account',
                            depends_on: 'eval:doc.reason == "Sold"',
                            mandatory_depends_on: 'eval:doc.reason == "Sold"',
                            get_query: () => {
                                return {
                                    filters: {
                                        disabled: 0,
                                        is_group: 0                  
                                    }
                                }
                            }
                        }
                    ],
                    (values) => {
                        console.log(values.reason)
                        frappe.confirm(
                            `Are you sure you want to save with reason: ${values.reason}?`,
                            () => {
                                frm.set_value("status", values.reason)
                                frm.save().then(() => {
                                    frm.call("sold", {
                                        debit_to: values.debit_to,
                                        customer: values.customer,
                                        income_account: values.income_account,
                                        reason: values.reason
                                    });
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
