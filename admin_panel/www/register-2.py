import frappe

def get_context(context):
    if frappe.form_dict.message:
        context.message = frappe.form_dict.message