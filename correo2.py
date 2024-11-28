import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass  # Para ocultar la contraseña al ingresarla

class CorreoElectronico:
    def __init__(self, remitente, contrasena):
        self.remitente = remitente
        self.contrasena = contrasena
        self.servidor_smtp = 'smtp.gmail.com'
        self.puerto_smtp = 587

    def enviar_correo(self, destinatario, asunto, cuerpo):
        try:
            # Crear el objeto del mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = self.remitente
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto

            # Adjuntar el cuerpo del mensaje
            mensaje.attach(MIMEText(cuerpo, 'plain'))

            # Conectar al servidor SMTP de Gmail
            servidor = smtplib.SMTP(self.servidor_smtp, self.puerto_smtp)
            servidor.starttls()  # Usar TLS para seguridad

            # Iniciar sesión en el servidor
            servidor.login(self.remitente, self.contrasena)

            # Enviar el mensaje
            servidor.sendmail(self.remitente, destinatario, mensaje.as_string())
            print("Correo enviado exitosamente")

            # Cerrar la conexión
            servidor.quit()
        except Exception as e:
            print(f"Ocurrió un error: {e}")

class AplicacionCorreo:
    def __init__(self):
        self.remitente = input("Introduce tu dirección de correo electrónico: ")
        self.contrasena = getpass.getpass("Introduce tu contraseña o contraseña de aplicación (si tienes 2FA activado): ")
        self.correo = CorreoElectronico(self.remitente, self.contrasena)

    def ejecutar(self):
        destinatario = input("Introduce la dirección de correo del destinatario: ")
        asunto = input("Introduce el asunto del correo: ")
        cuerpo = input("Introduce el cuerpo del mensaje: ")

        # Enviar el correo
        self.correo.enviar_correo(destinatario, asunto, cuerpo)

# Función principal
if __name__ == "__main__":
    app = AplicacionCorreo()
    app.ejecutar()
