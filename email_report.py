import json, smtplib, helper
from email.message import EmailMessage
from email.utils import make_msgid


class EmailReport:
    def __init__(self, csv_paths_list, csv_file_path, recipient):
        self.csv_paths_list = csv_paths_list
        self.csv_file_path = csv_file_path
        self.to_mail = recipient
        self.from_mail = ""
        self.from_password = ""
        self.smtp_server = ""
        self.smtp_port = 0
        self.date = helper.get_current_date()
        self.capture_type = helper.get_capture_type(self.csv_paths_list[0])

    def setup_email_properties(self):
        """
        The email details found in email_properties.json is a completely unused test email I made for testing
        purposes and the password is the app generated password for use with this script.  As mentioned elsewhere,
        in reality, I would have the user enter their email details in the Settings menu of this tool and save them
        as environment variables.
        :return:
        """
        # Open and read json file with email settings
        with open("data/email_properties.json") as email_file:
            email_data = json.load(email_file)

        # Settings
        self.from_mail = email_data["email_from_address"]
        self.from_password = email_data["email_from_password"]
        self.smtp_server = email_data["smtp_server_address"]
        self.smtp_port = email_data["smtp_server_port"]

    def create_email_body(self):
        # Set the email fields to the pre-established attributes.
        email = EmailMessage()
        email["Subject"] = f"[{self.date}] Asset Validation Report - {self.capture_type}"
        email["From"] = self.from_mail
        email["To"] = self.to_mail

        # Generate message IDs for each of the unique graph image plots that are to be embedded.
        image_cid = [make_msgid(idstring="first_img")[1:-1], make_msgid(idstring="second_img")[1:-1]]

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
                </body>
            </html>'
            '''.format(image_cid=image_cid, date=self.date, capture_type=self.capture_type), subtype="html"
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
