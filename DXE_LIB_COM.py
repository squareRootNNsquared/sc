import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time as t
import DXE_SC as sc
 
def email(subject,messageBody):
	###
	###	Sends an email via the DAX gmail account.
	###
	### Accepts a two string arguments sucht hat the
	### first is the subject and the second is the 
	### body of the message. The recipients are
	### specified externally by the list sc.par.mailList,
	### and are each emailed once with each execution.
	###
	###	Text messages may be sent via email. To do so,
	###	in place of the recipient, store the number 
	###	with _L appended such that "L" is the letter
	###	designated by this function to correspond to
	### the format of the SMS Gateway of the provider.
	###
	###	Example: recipient = "7894561230_A"
	###
	###	Note: SMS Gateway numbers are 10 digits, negl-
	###			ecting the common prepended "1", "+1"
	###
	###	AT&T: 		A [[Gateway confirmed, format OK]]
	###	Metro PCS:	M [[UNTESTED]]
	###	Sprint:		S [[UNTESTED]]
	###	T-Mobile:	T [[UNTESTED]]
	### Verizon:	V [[Gateway confirmed, potential format issues]]
	###	Virgin:		I [[Gateway confirmed, format OK]]
	###

	###
	###	Prevent empty messages from sending
	###
	if (messageBody != ""):

		###
		###	Perform function for each item in the mailing list
		###
		for r in range(0,len(sc.par.emailList)):

			###	Process phone number per specified provider
			phone = 0
			SMSG = {"A":"@txt.att.net","V":"@vtext.com","S":"@messaging.sprintpcs.com","T":"@tmomail.net","M":"@mymetropcs.com","I":"@vmobl.com"}
			if ("_" in sc.par.emailList[r]):
				if (sc.par.emailList[r].split("_")[0].isdigit()):
					if (sc.par.emailList[r].split("_")[1]):
						if (len(sc.par.emailList[r].split("_")[1]) == 1):
							number = sc.par.emailList[r].split("_")[0]
							gateway = sc.par.emailList[r].split("_")[1]
							gateway = SMSG[gateway]
							sc.par.emailList[r] = number + gateway
							phone = 1

			### Taxonomical Logistics
			sc_subjectPrepend 	= "DAXSC::"
			sc_subjectAppend	= "[[t_com=%s]]"%(t.strftime("%H:%M:%S"))
			fromaddr = "SlowControl.DAX.physics.UCD@gmail.com"
			toaddr = sc.par.emailList[r]
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = toaddr
			msg['Subject'] = sc_subjectPrepend + subject + sc_subjectAppend
			
			###	Core Message
			if (phone == 0):
				sc_signature =	"\n\n\n__________"+"\n__________\n"+"__________\n\n"+"This message was sent by the Davis Xenon Characterization Slow Control (DAXSC) workstation in the DAX lab at the University of California, Davis."
			if (phone == 1):
				sc_signature =	""
			body = messageBody + sc_signature
			msg.attach(MIMEText(body, 'plain'))
			
			### Digital Logistics
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(fromaddr, "_Ab0ve__ThE76TealPaSszionmUCK3")
			text = msg.as_string()
			server.sendmail(fromaddr, toaddr, text)
			server.quit()
