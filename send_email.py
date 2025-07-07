import smtplib #(Simple Mail Transfer Protocol).587/25
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox


def send_email():
    sender_email = email_entry.get()
    sender_password = password_entry.get()
    recipient_email = recipient_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END).strip()

    # Validate input fields
    if not all([sender_email, sender_password, recipient_email, subject, body]):
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        msg = MIMEMultipart() #to handle multiple parts of the email, including the subject, sender, recipient, and body.
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain')) #used to specify that the body of the email is in plain text format.

        server = smtplib.SMTP("smtp.gmail.com", 587) # 587 is tls port num 
        server.starttls() #starts TLS (Transport Layer Security) for encryption, 
        server.login(sender_email, sender_password) #logs in using the provided credentials,
        server.send_message(msg) #sends the email,
        server.quit() # closes the connection.

        messagebox.showinfo("Success", "Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Error", "Authentication failed. Check your email and password.")
    except Exception as e:
        messagebox.showerror("Error", f"Error sending email: {str(e)}")

# GUI for Sending Email
root = tk.Tk()
root.title("Send Email")
root.geometry("400x450")
root.configure(bg="#2C3E50")

def create_labeled_entry(root, label_text, show=""):
    frame = tk.Frame(root, bg="#2C3E50")
    frame.pack(pady=5, fill="x")
    tk.Label(frame, text=label_text, bg="#2C3E50", fg="white").pack(anchor="w")
    entry = tk.Entry(frame, bg="#ECF0F1", show=show)
    entry.pack(fill="x", padx=10, pady=3)
    return entry

# Pre-filled fields when TEST_MODE is enabled
email_entry = create_labeled_entry(root, "Your Email:")
password_entry = create_labeled_entry(root, "App Password:", show="*")
recipient_entry = create_labeled_entry(root, "Recipient Email:")
subject_entry = create_labeled_entry(root, "Subject:")

body_frame = tk.Frame(root, bg="#2C3E50")
body_frame.pack(pady=5, fill="x")
tk.Label(body_frame, text="Body:", bg="#2C3E50", fg="white").pack(anchor="w")
body_text = tk.Text(body_frame, height=5, bg="#ECF0F1")
body_text.pack(fill="x", padx=10, pady=3)

send_button = tk.Button(root, text="Send Email", command=send_email, bg="#2980B9", fg="white", width=15) #When clicked, it calls the send_email() function to send the email.
send_button.pack(pady=10)

root.mainloop()
