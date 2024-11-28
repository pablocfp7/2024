import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

# Clase para manejar el envío del correo
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
            servidor.quit()

            return True
        except Exception as e:
            return str(e)

# Clase para la interfaz gráfica
class AplicacionCorreo:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Envío de Correo")
        self.root.geometry("400x600")
        self.root.config(bg="#FF9933")  # Fondo gris claro

        # Elementos de la interfaz
        self.label_remitente = tk.Label(root, text="Correo Remitente:", bg="#f0f0f0", font=("Arial", 10))
        self.label_remitente.pack(pady=5)
        self.entry_remitente = tk.Entry(root, width=40, font=("Arial", 10))
        self.entry_remitente.pack(pady=5)

        self.label_contrasena = tk.Label(root, text="Contraseña:", bg="#f0f0f0", font=("Arial", 10))
        self.label_contrasena.pack(pady=5)
        self.entry_contrasena = tk.Entry(root, width=40, show="*", font=("Arial", 10))
        self.entry_contrasena.pack(pady=5)

        self.label_destinatario = tk.Label(root, text="Correo Destinatario:", bg="#f0f0f0", font=("Arial", 10))
        self.label_destinatario.pack(pady=5)
        self.entry_destinatario = tk.Entry(root, width=40, font=("Arial", 10))
        self.entry_destinatario.pack(pady=5)

        self.label_asunto = tk.Label(root, text="Asunto:", bg="#f0f0f0", font=("Arial", 10))
        self.label_asunto.pack(pady=5)
        self.entry_asunto = tk.Entry(root, width=40, font=("Arial", 10))
        self.entry_asunto.pack(pady=5)

        self.label_cuerpo = tk.Label(root, text="Cuerpo del mensaje:", bg="#f0f0f0", font=("Arial", 10))
        self.label_cuerpo.pack(pady=5)
        self.text_cuerpo = tk.Text(root, height=5, width=40, font=("Arial", 10))
        self.text_cuerpo.pack(pady=5)

        # Botón de envío con color de fondo
        self.boton_enviar = tk.Button(root, text="Enviar Correo", command=self.enviar_correo, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.boton_enviar.pack(pady=20)

    def enviar_correo(self):
        # Recoger datos de la interfaz
        remitente = self.entry_remitente.get()
        contrasena = self.entry_contrasena.get()
        destinatario = self.entry_destinatario.get()
        asunto = self.entry_asunto.get()
        cuerpo = self.text_cuerpo.get("1.0", tk.END)

        # Validaciones
        if not remitente or not contrasena or not destinatario or not asunto or not cuerpo:
            messagebox.showerror("Error", "Todos los campos deben ser completados")
            return

        # Crear instancia de la clase CorreoElectronico
        correo = CorreoElectronico(remitente, contrasena)

        # Enviar el correo
        resultado = correo.enviar_correo(destinatario, asunto, cuerpo)
        
        if resultado == True:
            messagebox.showinfo("Éxito", "Correo enviado exitosamente")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", f"Ocurrió un error: {resultado}")

    def limpiar_campos(self):
        self.entry_remitente.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
        self.entry_destinatario.delete(0, tk.END)
        self.entry_asunto.delete(0, tk.END)
        self.text_cuerpo.delete("1.0", tk.END)

# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()
    app = AplicacionCorreo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
