# Copyright (c) 2023, Hybrowlabs Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class FixedDepositControlRegister(Document):
    # def before_save(self):
    #     self.calculate_interest()

    # def calculate_interest(self):
    #     self.interest_amount = (self.amount_invested * self.rate_of_interest * self.no_of_days) / 36500
    #     self.net_interest = self.interest_amount - self.tds
    #     self.total_amount = self.amount_invested + self.interest_amount - self.tds

    def validate(self):
        if self.amount_invested <= 0:
            frappe.throw("Deposit Amount should be greater than zero")

        if self.rate_of_interest <= 0:
            frappe.throw("Rate of Interest should be greater than zero")

        if self.no_of_days <= 0:
            frappe.throw("Number of Days should be greater than zero")

        if frappe.utils.nowdate() > self.date_of_maturity:
            frappe.throw("Date of Maturity should be greater than Current Date")

    def on_update(self):
        frappe.msgprint("Fixed Deposit Control Register updated successfully!")

    def create_journal_entry(self):
        try:
            journal_entry = frappe.new_doc("Journal Entry")
            journal_entry.posting_date = frappe.utils.nowdate()
            journal_entry.company = self.company
            # journal_entry.voucher_type = (
            #     "Deferred Revenue" if doc.doctype == "Sales Invoice" else "Deferred Expense"
            # )
            # journal_entry.process_deferred_accounting = deferred_process
            total = (self.amount_invested+self.interest_amount)/100
            tds = total*10
            debit_bank_entry = {
                "account": self.bank_account,
                "credit_in_account_currency": (self.amount_invested+self.interest_amount)-tds,
            }
            debit_tds_entry = {
                "account": self.tds_account,
                "credit_in_account_currency": tds,
            }
            credit_interest_entry = {
                "account": self.interest_account,
                "debit_in_account_currency": self.interest_amount,
            }
            credit_fdr_entry = {
                "account": self.fdr_account,
                "debit_in_account_currency": self.amount_invested,
            }
            journal_entry.append("accounts", debit_bank_entry)
            journal_entry.append("accounts", debit_tds_entry)
            journal_entry.append("accounts", credit_interest_entry)
            journal_entry.append("accounts", credit_fdr_entry)
            journal_entry.cheque_no = self.name
            journal_entry.cheque_date = frappe.utils.nowdate()
            journal_entry.user_remark = "Auto created Entry for FDR"
            journal_entry.save()
            journal_entry.submit()
        except Exception:
            frappe.db.rollback()
            self.log_error(f"Error while processing deferred accounting for Invoice {self.name}")
            frappe.flags.deferred_accounting_error = True


def check_maturity():
    for item in frappe.get_all("Fixed Deposit Control Register",["name","date_of_maturity"]):
        from datetime import date
        days_to_maturity = (item.date_of_maturity - date.today()).days
        if days_to_maturity <= 7:
            frappe.db.set_value("Fixed Deposit Control Register",item.name,"before_one_week_of_the_maturity",True)
        if str(item.date_of_maturity) == str(frappe.utils.nowdate()):
            doc = frappe.get_doc("Fixed Deposit Control Register",item.name)
            if not frappe.get_value("Journal Entry",{"cheque_no":item.name},"name"):
                doc.create_journal_entry()
            
@frappe.whitelist()
def update_interest(doc,new_interest):
    frappe.db.set_value("Fixed Deposit Control Register",doc,"rate_of_interest",new_interest)

