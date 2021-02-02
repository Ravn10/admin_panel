## Admin Panel

Admin Panel

#### License

MIT
This is a template app to create custom website or webpages on erpnext

Step-1 
    Add all assets, js and css files to public folder


Step-2
    Create a base.html template file in templates/pages/ which will carry the desired theme that is commom to all pages
    include js files from frappe assets to make frappe.call work

    
Step-3
    Create Pages in www folder extending base.html
    write <page_name>.py file to render data from db to page or update page based on data passed on page
