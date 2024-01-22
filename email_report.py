import json, smtplib
from email.message import EmailMessage
from email.utils import make_msgid


class EmailReport:
    def __init__(self, plot_file_paths):
        self.plot_file_paths = plot_file_paths
        self.from_mail = ""
        self.from_password = ""
        self.smtp_server = ""
        self.smtp_port = 0
        self.to_mail = "gwongkmst@gmail.com"

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
        print(f"Plot File Paths: {self.plot_file_paths}")

        # Create the email message
        msg = EmailMessage()
        msg["Subject"] = "Art Asset Report"
        msg["From"] = self.from_mail
        msg["To"] = self.to_mail

        image_cid = [make_msgid(idstring="first_img")[1:-1], make_msgid(idstring="second_img")[1:-1]]

        # Attach HTML Body
        msg.set_content(
            '''
            <html>
                <body>
                    <h1 style="text-align: center;">Simple Data Report</h1>
                    <p>Here could be a short description of the data_old.</p>
                    <img src="cid:{image_cid[0]}">
                </body>
            </html>'
            '''.format(image_cid=image_cid), subtype="html"
        )

        for idx, imgtuple in enumerate([(self.plot_file_paths[0], "jpeg")]):
            imgfile, imgtype = imgtuple
            with open(imgfile, "rb") as plot_img:
                msg.add_related(
                    plot_img.read(),
                    maintype="image",
                    subtype=imgtype,
                    cid=f"<{image_cid[idx]}>"
                )

        return msg

    def finalize_send_email(self, msg):
        # Send the email
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.from_mail, self.from_password)
        server.sendmail(self.from_mail, self.to_mail, msg.as_string())
        server.quit()
