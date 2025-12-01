# Persona/Painpoint-Driven Outreach Engine (Email Automation Pipeline)

import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import openpyxl
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()  # This will read a .env file in the same folder

from email.mime.text import MIMEText
from datetime import datetime

# -----------------------------------------
# Simple reusable email sender
# -----------------------------------------

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email(recipient, body):
    msg = MIMEText(body)
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = "Personalized Outreach Email"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent to:", recipient)
        return True

    except Exception as e:
        print("Email failed:", e)
        return False

# -------------------------
# Initialize LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)


# LOAD EXCEL FILE
df = pd.read_excel("personas1.xlsx")

# Clean the Email Status column so empty cells are truly empty
df["Email Status"] = df["Email Status"].fillna("").astype(str).str.strip()


# Create Email Status column if missing
if "Email Status" not in df.columns:
    df["Email Status"] = ""   # empty values

prompt_template = PromptTemplate.from_template("""
Write an email in a technical tone with warmth and a human touch based on {persona} and {painpoint}.
The email should be hyper-personalized, start with Hi, {name}, and end with Regards, Jason.

The email must be exactly 5 lines.

STRICT RULES:
ONLY talk about the recipient’s listed painpoints.
Do NOT mention our internal needs or service offerings.
Do NOT invent any additional painpoints.
Provide one small early solution.
End the final line with a soft call to connect.

persona : {persona}
painpoint : {painpoint}
name : {name}
""")

# -------------------------
# PROCESS ONLY UNSENT ROWS
# -------------------------
for index, row in df.iterrows():

    # ❗ Send ONLY if Email Status is empty
    if str(row["Email Status"]).strip() != "":
        continue

    recipient_email = row["email"]

    # Generate prompt
    prompt = prompt_template.format(
        persona=row["Persona"],
        painpoint=row["painpoint1"],
        name=row["Name"]
    )

# response = llm.invoke(prompt)
# email_body = response.content

# For GitHub presentation, just simulate the email
email_body = f"Hi {row['Name']},\nThis is a sample email for {row['Persona']}."


    # If sent, update column
    if success:
        df.at[index, "Email Status"] = "Sent"
        df.at[index, "Sent Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nGenerated Email for:", row["Name"])
    print(email_body)
    print("-" * 60)

# SAVE FILE
df.to_excel("personas1.xlsx", index=False)

print("✔ Done. Only rows with empty 'Email Status' were processed.")
