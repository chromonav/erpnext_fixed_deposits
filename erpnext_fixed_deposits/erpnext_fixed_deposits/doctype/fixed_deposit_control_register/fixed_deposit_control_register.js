// Copyright (c) 2023, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Deposit Control Register', {
    refresh: function(frm) {
        // frm.add_custom_button(__('Update Maturity'), function(){
        //     var d = new frappe.ui.Dialog({
        //         'fields': [
        //             {
        //                 'fieldname': 'new_rate_of_interest',
        //                 'fieldtype': 'Float',
        //                 'label':"New Rate Of Interest"
        //             }
        //         ],
        //         primary_action: function(values){

        //             d.hide();
        //             frappe.call({
        //                 method:"erpnext_fixed_deposits.erpnext_fixed_deposits.doctype.fixed_deposit_control_register.fixed_deposit_control_register.update_interest",
        //                 args:{
        //                     doc:frm.selected_doc.name,
        //                     new_interest:values.new_rate_of_interest
        //                 },
        //                 callback: function(r) {
        //                     location.reload()
        //                 }
        //             })
        //             console.log(values.new_rate_of_interest)
        //             // console.log(typeof values.new_rate_of_interest)
        //             // frappe.db.set_value("Fixed Deposit Control Register",frm.selected_doc.name,"rate_of_interest",values.new_rate_of_interest)
        //         }
        //     });
        //     d.show();
        // });
    },
    onload: function(frm) {
        frm.set_query("bank_account", function() {
            return {
                filters: {
					'company':frm.selected_doc.company,
                    'is_group':0,
                    'account_currency':"INR"
                }
            };
        });
        frm.set_query("tds_account", function() {
            return {
                filters: {
					'company':frm.selected_doc.company,
                    'is_group':0,
                    'account_currency':"INR"
                }
            };
        });
        frm.set_query("interest_account", function() {
            return {
                filters: {
					'company':frm.selected_doc.company,
                    'is_group':0,
                    'account_currency':"INR"
                }
            };
        });
        frm.set_query("fdr_account", function() {
            return {
                filters: {
					'company':frm.selected_doc.company,
                    'is_group':0,
                    'account_currency':"INR"
                }
            };
        });
    }
});

