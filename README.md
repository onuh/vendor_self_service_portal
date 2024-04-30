# About
This is a Vendor Self service portal module for Fatmug Designs. It allows a vendor to view and download a number or all upcoming product demand forcast for the next quater (3 months) in PDF and excel format from their dashboards and also submit an order adjustment request for existing sales order to the procurement team. The procurement team will receive an email each time a portal vendor user submits a sale order adjustment report.

# Module Dependency
For the module to be installed and function properly, the following dependency must exist already installed. Dependencies are configured in the manifest file ![Manifest File](__manifest__.py)
- `Sales Module`.
- `Portal Module`.
- `Product Module`

# Third Party Plugins
Third party css and Javascript plugins were used for this project. This files are found in ![CSS folder](static/src/css) and ![Javascript Folder](static/src/css). The plugins includes:
- `alertify` which gives alert notification on the portal. Link to the plugin is found here: ![Alertify Plugin](http://alertifyjs.com)
- `WaitMe` which shows a loader for certain events on portal. We used this instead of odoo's `web.framework`. Link to the plugin is found here: ![WaitMe](https://github.com/vadimsva/waitMe)
- `Selectize` which allows vendor to quickly search for a sale order in select field during sale order adjustment request submission. Link to the plugin is found here: ![Selectize](https://github.com/selectize)
- `colorlib-wizard-5 html step template` which allows for stepwise collection of data from vendor during sale order adjustment request. The plugin comes with Jquery steps plugin and other css plugin. Link to the plugin is found here: ![Colorlib-wizard-5](https://colorlib.com/wp/template/colorlib-wizard-5/)

# Access Rights and Security rules
The portal user who is a vendor ordinarily do not have access to certain odoo models. For the module to function properly, read access was granted to the following models. This is implemented in ![Access Rights](security/ir.model.access.csv)
- `vendor.adjustment.request`.
- `vendor.forecast`.
- `product.product`
- `product.template`
- `ir.actions.report`

# Installation of Module
Ensure that all dependency modules are available on your odoo system. Then clone this repository. Ensure that all files are in a folder named `vendor_self_service_portal`.
* Move the folder to odoo custom addons directory on server
* Restart the odoo service
* Login as admin with settings access rights and enable the debug mode from settings
* From apps menu, click on update module list
* Search for `vendor_self_service_portal`, then click on activate to install


# How to use
- Login as admin and add product forcast from the sales app menu `Product Forecast` ![Product Forcast](images/Screenshot_from_2024-04-29_21-12-52.png).
- Login as a Vendor Portal user to see added menu for submission of sales order adjustment request and upcomng demand forcast ![Added Menu To Portal user](images/Screenshot_from_2024-04-29_21-22-58.png).
- As A Vendor, click on `Order Adjustment` to submit an Order Adjustment or `Product Forcast` to see upcoming product demand forcast.
	# Order Adjustment
	- Select a sale order number and click on `Next` to progress the step wizard ![Step 1 wizard](images/Screenshot_from_2024-04-29_21-17-40.png)
	- Enter Adjustment to order and click on `Next` to progress the wizard ![Step 2 wizard](images/Screenshot_from_2024-04-29_20-51-02.png)
	- Enter an Addition comment to progress wizard to the last stage ![Step 3 wizard](images/Screenshot_from_2024-04-29_20-51-41.png)
	- As a last step, click on submit request to send your request and procurement team members receive email to that effect.![Step 4 wizard](images/Screenshot_from_2024-04-29_20-52-34.png)
	- Procurement Team members receive emails ![Email Received](images/Screenshot_from_2024-04-29_21-19-22.png)
	- Procurement team member login to backend to see adjustment request in the `Adjustment Request` Menu from sales app, click on sale order to open form view to see details that needs to be adjusted and proceed to make the adjustment. ![Backend Adjustment Request](images/Screenshot_from_2024-04-29_20-54-10.png)

	# Upcoming Product Demand Forcast
	- click on first checkbox to select all forcast displayed on page or click on any of the checkbox for any product, then select a format to download, then click on `Generate Report` button ![Forcast View](images/Screenshot_from_2024-04-29_21-13-58.png) ![Report Generation](images/Screenshot_from_2024-04-29_21-14-18.png) ![PDF Report](images/Screenshot_from_2024-04-29_21-14-58.png) ![Excel Report](images/Screenshot_from_2024-04-29_21-15-36.png)