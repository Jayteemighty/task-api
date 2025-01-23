import smtplib
from pathlib import Path
import os
from dotenv import load_dotenv

class Util:
    '''Utility class'''
    
    @staticmethod
    def send_email(email, subject, body):
        '''
        Function to send verification email to a user;s email
        '''
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(os.path.join(BASE_DIR, ".env"))
        
        EMAIL_HOST_USER = os.getenv('MY_EMAIL')
        EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')
        
        with smtplib.SMTP('smtp.gmail.com', 587) as conn:
            conn.starttls()
            conn.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
            
            conn.sendmail(
                from_addr=EMAIL_HOST_USER, 
                to_addrs=email,
                msg=f"Subject:{subject}\n\n{body}"
            )
    
    @staticmethod
    def send_update(user_email, task_name):
        '''
        Function to send an email notification when a task is marked as complete.
        '''
        subject = "Task Status Update"
        body = f'Your task "{task_name}" has been marked as complete.'
        
        Util.send_email(user_email, subject, body)
