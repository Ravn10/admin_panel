import frappe
from frappe.core.doctype.user.user import sign_up

def get_context(context):
    context.no_cache = 1
    context.title = "Register"
    context.message ="Hi this is message"
    context.submitted = False
    frappe.msgprint("Hekki")
    context.form_2="block"
    context.form_2="none"
    if frappe.form_dict.first_name:
        first_name = frappe.form_doct.first_name
        email = frappe.form_doct.email
        context.message = frappe.form_dict.first_name
        context.message = create_lead(frappe.form_dict.first_name)

    if email:
        sign_up(email=email,full_name=full_name,redirect_to='')
        context.form_2 = "block"
        context.form_1="none"
        
@frappe.whitelist(allow_guest=True)
def create_lead(full_name):
    doc = frappe.get_doc({        
    "doctype": "Lead",
    "lead_name": full_name
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name
