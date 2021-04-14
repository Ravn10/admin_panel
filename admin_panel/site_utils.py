import frappe
from frappe.model.document import Document
from subprocess import check_output, Popen, PIPE
import os, re, json, time, pymysql, shlex
from bench_manager.bench_manager.utils import verify_whitelisted_call, safe_decode
from frappe.utils.password import get_decrypted_password
from bench_manager.bench_manager.doctype.site.site import create_site
import subprocess
from bench_manager.bench_manager.utils import run_command

@frappe.whitelist()
def create_site_for_saas(site_name, install_erpnext, key, domain):
    mysql_password = get_decrypted_password("SAAS Settings","SAAS Settings","db_password")
    admin_password = get_decrypted_password("SAAS Settings","SAAS Settings","admin_password")
    admin_password = frappe.db.get_single_value("SAAS Settings","default_admin_pwd")
    custom_domain = domain + "."+ frappe.db.get_single_value("SAAS Settings","saas_domain")
    create_site(site_name, install_erpnext, mysql_password, admin_password, key,domain)

def update_custom_domain(doc, method=None):
    key =str(frappe.utils.datetime.datetime.now())
    domain = doc.domain
    site_name = doc.name
    doctype = "SAAS Settings"
    commands = ["bench setup add-domain {domain} --site {site_name}".format(domain=domain, site_name=site_name)]
    run_command(commands, doctype, key, cwd='..', docname=' ')
    frappe.msgprint(commands)
    subprocess.call("sudo service nginx reload", shell=True)

def update_customer_email(doc):
    contacts = frappe.get_all('Contact',filters=[
                                    ['Dynamic Link','link_doctype','=','Customer'],
                                    ["Dynamic Link", "link_name", "=",doc.name],
                                    ["Dynamic Link", "parenttype", "=", "Contact"]
                                    ],
                            fields=["name",'email_id','mobile_no']
                    )
    if contacts:
        contact = contacts[0]
        doc.customer_primary_contact = contact.name
        doc.mobile_no = contact.mobile_no
        doc.email_id = contact.email_id
        doc.save()
        
def send_email_on_site_creation(doc,method=None):
    if doc.status == "Success":
        frappe.publish_progress(
			99  / 100,
			title = "Site Created",
			description = "Site Created"
		)
    else:
        frappe.publish_progress(
			99  / 100,
			title = "Site Not Created",
			description = "Site Not Created"
		)