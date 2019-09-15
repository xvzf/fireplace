from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def sendEmail(recp, subject, body):
	fromaddr = "vs19mon@gmail.com"
	if (len(recp) == 0): recp = "laurent@ludwig.lu"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = recp
	msg['Subject'] = "VS19 Monitor: " + subject
	msg.attach(MIMEText(body, 'plain'))

	uname = "vs19mon"
	passwd = "Vs19MonBot"
	server = smtplib.SMTP('smtp.gmail.com', 587)

	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login(uname, passwd)
	text = msg.as_string()
	server.sendmail(fromaddr, recp, text)
	server.quit()

#sendEmail("", "Überschreitung der Maximaltemperatur festgestellt", "Der Sensor SENSOR hat um UHRZEIT Uhr die Maximaltemperatur von MAXTEMP überschritten.")