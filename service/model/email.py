from ..config.config import Config
from .decorators import debug
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl


class Mail(Config):
    """
    This class sends an email with an attachment.
    """

    def __init__(self):
        Config.__init__(self)
        self.port = 587
        self.smtp_server = "smtp.gmail.com"
        self.sesclient = self.get_boto_client('ses')

    def html(self, summary: dict) -> str:
        """This function creates an html view for displaying the information."""
        def concat_months():
            """This functions creates a new entry for a parragraph containing monthly information."""
            months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
            return '<br>'.join(list(map(
                lambda x: f"Number of transactions in {months[x]}: {summary['monthlysummary'][x]['CountTransaction']}", summary['monthlysummary'])))

        return f"""
            <html>
            <body>
            <a>
                <img src="https://media-exp1.licdn.com/dms/image/C4E0BAQHtxnxSv1F2HQ/company-logo_200_200/0/1562253639430?e=2159024400&v=beta&t=OTPUGauJAaVkkW2Uc1pZS9Qj_AHMCC2nbqt2ttvR6uE"
                width=150 height=150>
            </a>
                <p>Stori, Balance Information<br>
                </p>
                <p>
                    Total balance is: {summary['generalsummary']['TotalBalance']}<br>
                    Average debit amount: {summary['generalsummary']['AvgD']}<br>
                    Average credit amount: {summary['generalsummary']['AvgC']}<br>
                    {concat_months()}
                </p>
            </body>
            </html>
        """

    def new_mail(self, summary: dict):
        """This function constructs an email with an attachment, and sends it through SMTP."""
        
        receiver_email = "franciscohsepulveda@gmail.com"
        
        msg = MIMEMultipart()
        msg['Subject'] = 'This is an email with an attachment!'
        msg['From'] = self.SENDER
        msg['To'] = self.SENDER

        part = MIMEText(self.html(summary), "html")
        msg.attach(part)

        filename = '/tmp/summary.csv'

        with open(filename, 'rb') as attachment:
            part2 = MIMEApplication(attachment.read())
            part2.add_header('Content-Disposition',
                             'attachment',
                             filename="summary.csv")
        msg.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.SENDER, self.PASSWORD)
            server.sendmail(self.SENDER, receiver_email, msg.as_string())
