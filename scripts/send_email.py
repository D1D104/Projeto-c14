import os
import smtplib
from email.mime.text import MIMEText

def main():
    to_email = os.environ.get('NOTIFY_EMAIL')
    if not to_email:
        print('NOTIFY_EMAIL não definido')
        exit(1)
    from_email = os.environ.get('FROM_EMAIL', to_email)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')

    msg = MIMEText('Pipeline executado!')
    msg['Subject'] = 'Status da Pipeline'
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, [to_email], msg.as_string())
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
        exit(1)

if __name__ == '__main__':
    main()