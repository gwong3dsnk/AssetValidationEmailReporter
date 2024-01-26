import json, smtplib, helper, os
from email.message import EmailMessage
from email.utils import make_msgid


class EmailReport:
    def __init__(self, csv_paths_list, csv_file_path, recipient, full_line_report):
        self.csv_paths_list = csv_paths_list
        self.csv_file_path = csv_file_path
        self.to_mail = recipient
        self.from_mail = ""
        self.from_password = ""
        self.smtp_server = ""
        self.smtp_port = 0
        self.date = helper.get_current_date()
        self.capture_type = helper.get_capture_type(self.csv_paths_list[0])
        self.critical_fails = full_line_report[0]
        self.high_fails = full_line_report[1]
        self.medium_fails = full_line_report[2]

    def setup_email_properties(self):
        """
        Set the email properties
        :return: (bool) if email details are missing.
        """
        working_dir, proj_data_dir = helper.get_working_dir_path()
        json_file = os.path.join(proj_data_dir, "sender_email_data.json")

        # Open and read json file with email settings
        with open(json_file, "r") as email_file:
            email_data = json.load(email_file)
            if (email_data["email_from_address"] == "" or email_data["email_from_password"] == "" or
                    email_data["smtp_server_address"] == "" or email_data["smtp_server_port"] == ""):
                return False
            else:
                self.from_mail = email_data["email_from_address"]
                self.from_password = email_data["email_from_password"]
                self.smtp_server = email_data["smtp_server_address"]
                self.smtp_port = email_data["smtp_server_port"]
                return True

    def create_email_body(self):
        """
        Create the email HTML body contents of the report
        :return:
        """
        # Set the email fields to the pre-established attributes.
        email = EmailMessage()
        email["Subject"] = f"[{self.date}] Asset Validation Report - {self.capture_type}"
        email["From"] = self.from_mail
        email["To"] = self.to_mail

        # Generate message IDs for each of the unique graph image plots that are to be embedded.
        image_cid = [make_msgid(idstring="first_img")[1:-1], make_msgid(idstring="second_img")[1:-1]]
        critical_fails = "<br />\n".join(self.critical_fails)
        high_fails = "<br />\n".join(self.high_fails)
        medium_fails = "<br />\n".join(self.medium_fails)

        # Create the HTML body text with formatting
        email.set_content(
            '''
            <html>
                <body>
                    <h1 style="text-align: center;">Asset Data Validation Report</h1>
                    <p>Ladies and Gents, here is today's latest report on the health of our art library.
                    This is just a quick overview of the state of things.  Refer to the attachment to see the source 
                    data CSV files in order to conduct a deeper review.</p>
                    <p>If you have any questions, please don't hesitate to reach out to Tech Art.  Much obliged!</p>
                    <h3>Date of Report: {date}</h3>
                    <h3>Capture Type: {capture_type}</h3>
                    <p>This first chart shows an overview of how many of each failed asset exists 
                    per level of Severity.</p>
                    <img src="cid:{image_cid[0]}"></img><br>
                    <p>This next chart displays, out of all failed assets, what percentage of them fell into which
                    category of failure.</p>
                    <img src="cid:{image_cid[1]}"></img>
                    <p>Refer to the attachment to see the source data CSV files in order to conduct a deeper review.</p>
                    <h2>Asset List</h2>
                    <h3>Critical Failures</h3>
                    <p>{critical_fails}</p>
                    <h3>High Failures</h3>
                    <p>{high_fails}</p>
                    <h3>Medium Failures</h3>
                    <p>{medium_fails}</p>
                </body>
            </html>
            '''.format(
                image_cid=image_cid,
                date=self.date,
                capture_type=self.capture_type,
                critical_fails=critical_fails,
                high_fails=high_fails,
                medium_fails=medium_fails
            ), subtype="html"
        )

        # Embed the generated graph plots into the email body.
        for idx, imgtuple in enumerate([(self.csv_paths_list[0], "jpg"), (self.csv_paths_list[1], "jpg")]):
            imgfile, imgtype = imgtuple
            with open(imgfile, "rb") as plot_img:
                email.add_related(
                    plot_img.read(),
                    maintype="image",
                    subtype=imgtype,
                    cid=f"<{image_cid[idx]}>"
                )

        # Attach the source CSV file to the email.
        with open(self.csv_file_path, "rb") as csv_file:
            csv = csv_file.read()
            email.add_attachment(
                csv,
                maintype="application",
                subtype="csv",
                filename=f"{self.capture_type}.csv"
            )

        return email

    def finalize_send_email(self, email):
        # Send the email
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.from_mail, self.from_password)
        server.sendmail(self.from_mail, self.to_mail, email.as_string())
        server.quit()
