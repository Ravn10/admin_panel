import frappe
from frappe.core.doctype.user.user import sign_up, send_token_via_email
from frappe.twofactor import authenticate_for_2factor
from admin_panel.site_utils import create_site_for_saas

def get_context(context):
    # context.csfr = frappe.generate_hash()
    context.company_domain = frappe.db.get_single_value("SAAS Settings","saas_domain")
    frappe.local.session.data.csrf_token = frappe.generate_hash()
    context.no_cache = 1
    context.title = "Register"
    context.message ="Hi this is message"
    context.submitted = False
    context.form_2="block"
    context.form_2="none"
    context.form_3="none"
    context.form_4 = "none"
    context.thanks = "none"
    email = ''
    mobile_no = None
    if frappe.form_dict.site:
        frappe.local.session.data.site = frappe.form_dict.site
    if frappe.form_dict.phone:
        mobile_no = frappe.form_dict.phone
    if frappe.form_dict.first_name:
        first_name = frappe.form_dict.first_name
        email = frappe.form_dict.email
        frappe.local.session.data.site = frappe.form_dict.subdomain
        site_name = context.site = frappe.form_dict.subdomain
        context.message = frappe.form_dict.first_name
        context.message = create_customer(frappe.form_dict.first_name,email,site_name,mobile_no)
        key =format(frappe.utils.datetime.date.today())
        frappe.local_cache.site = frappe.form_dict.subdomain
        # context.message = create_lead(frappe.form_dict.first_name,email)
        # context.token_sent = send_token_via_email(email,token)
        context.form_2 = "block"
        context.form_1="none"
        context.form_3="none"
        context.thanks = "none"
        context.form_4 = "none"
    if email:
        context.status , context.signup_msg = sign_up(email=email,full_name=first_name,redirect_to='/register?form_3=true&site='+frappe.form_dict.subdomain)
        context.form_2 = "block"
        context.form_1="none"
        context.form_3="none"
        context.form_4 = "none"
        context.thanks = "none"
        # if status == 0:
            
    if frappe.form_dict.form_3:
        context.form_1="none"
        context.form_2="none"
        context.form_3 = "block"
        context.form_4 = "none"
        context.thanks = "none"

    if frappe.form_dict.timezone:
        context.form_1="none"
        context.form_2="none"
        context.form_3 = "none"
        context.form_4 = "block"
        context.thanks = "none"

    if frappe.form_dict.users:
        if int(frappe.form_dict.users)>0:
            context.form_1="none"
            context.form_2="none"
            context.form_3 = "none"
            context.thanks = "block"
            context.title = context.site = frappe.local.session.data.site
            # site_name = get_site_name(frappe.session.user)
            create_site_for_saas(site_name=frappe.local.session.data.site,install_erpnext=True,
                                key=format(frappe.utils.datetime.date.today()),
                                domain=frappe.local.session.data.site)


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
def create_customer(full_name,email,site,mobile_no=None):
    if not frappe.get_all("Customer",filters={'email_id':email},fields=['name']):
        doc = frappe.get_doc({        
        "doctype": "Customer",
        "customer_name": full_name,
        "email_id":email,
        "mobile_no":mobile_no,
        "site":site
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