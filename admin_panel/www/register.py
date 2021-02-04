import frappe

def get_context(context):
    context.logo = frappe.db.get_single_value("Website Settings",'banner_image')
    context.tagline = frappe.db.get_single_value("Website Settings",'tag_line')
    context.favicon = frappe.db.get_single_value("Website Settings",'favicon')
    context.brand_html = frappe.db.get_single_value("Website Settings",'brand_html')

@frappe.whitelist()
def create_customer(email,mobile_no=None):
    frappe.local.flags.redirect_location = "/contact"
    customer = frappe.get_doc({
        "doctype":"Customer",
        "customer_name":email,
        "type":"Company",
        "mobile_no":mobile_no or ''
        }).insert(ignore_permissions=True)
    return customer.name