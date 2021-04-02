import frappe

def get_context(context):
    # innovation_category = frappe.sql_list('''select name from `tabInnovation Category` ''')
    context.users = frappe.db.sql_list(''' select full_name from tabUser''')