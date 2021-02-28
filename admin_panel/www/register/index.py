import frappe
from frappe.core.doctype.user.user import sign_up, send_token_via_email
from frappe.twofactor import authenticate_for_2factor

def get_context(context):
    frappe.local.session.data.csrf_token = frappe.generate_hash()
    context.no_cache = 1
    context.title = "Register"
    context.message ="Hi this is message"
    context.submitted = False
    context.form_2="block"
    context.form_2="none"
    context.form_3="none"
    email = ''
    if frappe.form_dict.first_name:
        first_name = frappe.form_dict.first_name
        email = frappe.form_dict.email
        context.message = frappe.form_dict.first_name
        context.message = create_lead(frappe.form_dict.first_name,email)
        # context.token_sent = send_token_via_email(email,token)
        context.form_2 = "block"
        context.form_1="none"
        context.form_3="none"
    if email:
        context.status , context.signup_msg = sign_up(email=email,full_name=first_name,redirect_to='/register?form_3=true')
        context.form_2 = "block"
        context.form_1="none"
        context.form_3="none"
        # if status == 0:
            
    if frappe.form_dict.form_3:
        context.form_1="none"
        context.form_2="none"
        context.form_3 = "block"

@frappe.whitelist(allow_guest=True)
def create_lead(full_name,email):
    if not frappe.get_all("Lead",filters={'email_id':email},fields=['name']):
        doc = frappe.get_doc({        
        "doctype": "Lead",
        "lead_name": full_name,
        "email_id":email
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc.lead_name
    else:
        return frappe.get_all("Lead",filters={'email_id':email},fields=['lead_name'])

@frappe.whitelist(allow_guest=True)
def create_site(site_name):
    pass

def validate_domain(domain):
    pass