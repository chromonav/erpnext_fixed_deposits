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


def check_maturity():
    for item in frappe.get_all("Fixed Deposit Control Register",["name","date_of_maturity"]):
        from datetime import date
        days_to_maturity = (item.date_of_maturity - date.today()).days
        if days_to_maturity <= 7:
            frappe.db.set_value("Fixed Deposit Control Register",item.name,"before_one_week_of_the_maturity",True)