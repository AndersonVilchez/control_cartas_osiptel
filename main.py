
import imaplib
import email
from email.header import decode_header
import pandas as pd

# Conexión al correo
IMAP_SERVER = "imap.gmail.com"  # Cambiar si no usas Gmail
EMAIL = "anderson.vilchez@telefonica.com"
PASSWORD = "tu_contraseña"

# Conectar al servidor
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Seleccionar carpeta INBOX
mail.select("inbox")

# Buscar correos con "OSIPTEL" en el asunto
status, messages = mail.search(None, 'SUBJECT "OSIPTEL"')
emails = messages[0].split()

# Tabla para almacenar la información
data = []

for email_id in emails:
    # Fetch del correo
    res, msg = mail.fetch(email_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # Obtener fecha y asunto
            date = msg["Date"]
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()  # Decodificar bytes
            # Extraer contenido (si está en texto plano)
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # Agregar datos a la tabla
            data.append({
                "Fecha de Notificación": date,
                "Asunto": subject,
                "Nombre de Carta": subject.split("-")[0],  # Suponiendo formato
                "Hora": date.split()[4]
            })

# Crear DataFrame
df = pd.DataFrame(data)
df.to_csv("cartas.csv", index=False)  # Guardar para consulta
mail.logout()
