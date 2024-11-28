import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(remitente, destinatario, asunto, cuerpo, contrasena):
    try:
        # Configuración del servidor SMTP de Gmail
        servidor_smtp = 'smtp.gmail.com'
        puerto_smtp = 587

        # Crear el objeto de mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto

        # Adjuntar el cuerpo del mensaje
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Conectar al servidor SMTP de Gmail
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()  # Usar TLS para seguridad

        # Iniciar sesión en el servidor
        servidor.login(remitente, contrasena)

        # Enviar el mensaje
        servidor.sendmail(remitente, destinatario, mensaje.as_string())

        print("Correo enviado exitosamente")

        # Cerrar la conexión
        servidor.quit()
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Función principal
def main():
    # Solicitar información al usuario
    remitente = input("Introduce tu dirección de correo electrónico: ")
    destinatario = input("Introduce la dirección de correo del destinatario: ")
    asunto = input("Introduce el asunto del correo: ")
    cuerpo = input("Introduce el cuerpo del mensaje: ")
    contrasena = input("Introduce tu contraseña o contraseña de aplicación (si tienes 2FA activado): ")

    # Llamar a la función para enviar el correo
    enviar_correo(remitente, destinatario, asunto, cuerpo, contrasena)

if __name__ == "__main__":
    main()
