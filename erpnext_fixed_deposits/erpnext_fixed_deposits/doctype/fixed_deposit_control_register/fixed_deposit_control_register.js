// Copyright (c) 2023, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Deposit Control Register', {
	refresh: function(frm) {
		frm.add_custom_button(__('Upadate Interest'), function(){
			var d = new frappe.ui.Dialog({
				'fields': [
					{
						'fieldname': 'new_rate_of_interest',
						'fieldtype': 'Float',
						'label':"New Rate Of Interest"
					}
				],
				primary_action: function(values){

					d.hide();
					console.log(values.new_rate_of_interest)
					frappe.db.set_value("Fixed Deposit Control Register",frm.selected_doc.name,"rate_of_interest",values.new_rate_of_interest)
				}
			});
			d.show();
		});
	}
});

