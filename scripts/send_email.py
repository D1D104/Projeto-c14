import os
import smtplib
from email.mime.text import MIMEText

def main():
    to_email = os.environ.get('NOTIFY_EMAIL')
    from_email = os.environ.get('FROM_EMAIL')
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')

    if not all([to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_pass]):
        print('Variáveis de ambiente para envio de email não definidas. Pulando envio de email.')
        return

    msg = MIMEText('Pipeline executado!')
    msg['Subject'] = 'Status da Pipeline'
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, [to_email], msg.as_string())
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
        return

if __name__ == '__main__':
    main()