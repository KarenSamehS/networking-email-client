import imaplib # Uses IMAP protocol to fetch the latest email.(993)(143)
import email
import tkinter as tk
from tkinter import messagebox
from plyer import notification #Sends desktop notifications f

def receive_email():
        
    email_address = email_entry.get()
    password = password_entry.get()
    
    if not email_address or not password:
        messagebox.showerror("Error", "Please enter both email address and password.")
        return
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993) #Connects securely to Gmail using SSL (port 993).security socket layer 
        mail.login(email_address, password)
        mail.select("inbox") #Selects the "inbox" to read emails.

        result, data = mail.search(None, "ALL") #Searches for all emails in the inbox.
        if result != "OK" or not data[0]:
            messagebox.showinfo("Info", "No emails found.")
            return

        latest_email_id = data[0].split()[-1] #Picks the latest one (last ID in the list).
        result, data = mail.fetch(latest_email_id, "(RFC822)") #Fetches the full email content in RFC822 format.
        if result != "OK":
            messagebox.showerror("Error", "Failed to fetch email.")
            return

        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email) #Converts raw byte data to an actual email object.
        subject = email_message['Subject']
        sender = email_message['From']

    #If the email has multiple parts (e.g. attachments), extract only the plain text body.
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        notification.notify(
            title=f"New Email from {sender}",
            message=f"Subject: {subject}\n{body[:50]}...",
            timeout=5
        )

        messagebox.showinfo("New Email", f"From: {sender}\nSubject: {subject}\nBody:\n{body}")

        mail.close()
        mail.logout()
    except imaplib.IMAP4.error as e:
        messagebox.showerror("Error", f"IMAP error: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error receiving email: {str(e)}")

# GUI for Receiving Email
root = tk.Tk()
root.title("Receive Email")
root.geometry("400x300")
root.configure(bg="#2C3E50")

email_entry = tk.Entry(root, bg="#ECF0F1")
email_entry.pack(pady=10)
email_label = tk.Label(root, text="Email Address", bg="#2C3E50", fg="white")
email_label.pack()

password_entry = tk.Entry(root, bg="#ECF0F1", show="*")
password_entry.pack(pady=10)
password_label = tk.Label(root, text="App Password", bg="#2C3E50", fg="white")
password_label.pack()

receive_button = tk.Button(root, text="Check Email", command=receive_email, bg="#2980B9", fg="white")
receive_button.pack(pady=20)

root.mainloop()
