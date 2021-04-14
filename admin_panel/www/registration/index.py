import frappe
from frappe.core.doctype.user.user import sign_up, send_token_via_email
from frappe.twofactor import authenticate_for_2factor
from admin_panel.site_utils import create_site_for_saas

def get_context(context):
    context.form_1 = "block"
    context.csfr = frappe.generate_hash()
    frappe.local.session.data.csrf_token = frappe.generate_hash()
    context.no_cache = 1
    context.title = "Register"
    email = ''
    mobile_no = None
    full_name = None
    if frappe.form_dict.phone:
        mobile_no = frappe.form_dict.phone
    if frappe.form_dict.first_name:
        first_name = frappe.form_dict.first_name
    if frappe.form_dict.last_name:
        last_name = frappe.form_dict.last_name
    if first_name and last_name:
        full_name = first_name + " " + last_name
    else:
        full_name = first_name
    if frappe.form_dict.email:
        email = frappe.form_dict.email
        context.status , context.signup_msg = sign_up(email=email,full_name=full_name,redirect_to='/prepare_site')
        if not context.status:
            context.form_1 = "none"
  
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
def create_customer(full_name,email,mobile_no=None):
    if not frappe.get_all("Customer",filters={'email_id':email},fields=['name']):
        doc = frappe.get_doc({        
        "doctype": "Customer",
        "customer_name": full_name,
        "email_id":email,
        "mobile_no":mobile_no
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc.customer_name
    else:
        return frappe.get_all("Customer",filters={'email_id':email},fields=['customer_name'])

@frappe.whitelist(allow_guest=True)
def validate_domain(subdomain):
    if frappe.db.exists("Site",subdomain):
        return True
    else:
        return False