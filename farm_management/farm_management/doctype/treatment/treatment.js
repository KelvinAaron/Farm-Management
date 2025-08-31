// Copyright (c) 2025, Group 2 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Treatment", {
    refresh(frm) {
        frm.toggle_enable("product_details", frm.doc.warehouse);

        // Only list warehouses that have products in stock.
        frappe.db.get_list("Bin", {
            fields: ["warehouse", "actual_qty"],
        }).then(bins => {
            bins = bins.filter(i => i.actual_qty > 0)
            bins = [...new Set(bins.map(i => i.warehouse))]

            frm.set_query("warehouse", () => {
                return {
                    filters: {
                        "name": ["in", bins]
                    }
                }
            })

        })

    },
    warehouse(frm) {
        frm.toggle_enable("product_details", frm.doc.warehouse);
        frm.set_value("product_details", "")

        // Filter items only in the specified warehouse.
        frappe.db.get_list("Bin", {
            fields: ["item_code"],
            filters: {
                warehouse: frm.doc.warehouse,
                actual_qty: [">", 0]
            }
        }).then(bins => {
            frm.set_query("product_details", () => {
                return {
                    filters: {
                        "item_name": ["in", bins.map(i => i.item_code)]
                    }
                }
            })
        })
    },
});
