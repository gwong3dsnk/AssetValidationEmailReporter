# Purpose
This code is purely for practice with matplotlib, tkinter, EmailMessage, json and pandas

# Intended Use
The Asset Validation Email Reporter is intended to intake csv files containing 3d game asset data.  In a spreadsheet (Excel, Google etc), data could included asset triangle count, the company triangle budget, how many LODs the asset has, what the LOD budget is, and so on.  It will parse the csv data and generate visual graph reports.  These reports are intended to be sent to anyone in a company who is interested in the overall health of the art asset library and the game project.  Intended viewers are those in art, tech art, and engineers.  The user of the tool can insert email addresses and send an email report to the intended recipients.

# Why is this useful?
You can take data from hundreds of assets, perhaps even thousands, compress them into an easy-to-read visual graph, and allow viewers to get a quick overview on the health of the game art library and the game itself.  Artists in particular won't have to dig through data and numbers and errors, and just see the summary report.

# How to use the tool
The steps are outlined in the tool GUI.
Step 1 is to drag and drop 1 or more csv files into the listbox
Optional Step is to click on Preview Graph to see what the generated graphs will look like
Step 2 is to add email addreses to the intool address book by typing in the text field then hitting Enter on the keyboard
Step 3 is to add the recipient(s) email address(es) to the Recipient listbox using the arrow buttons.  The email addresses in the right listbox will receive the emails.
Step 4 is to Send the Email Report
