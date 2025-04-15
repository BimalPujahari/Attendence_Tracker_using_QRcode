import qrcode

def generate_qr(session_code, local_ip="192.168.1.7", port=8501):
    full_url = f"http://{local_ip}:{port}/?session={session_code}"
    img = qrcode.make(full_url)
    filename = f"{session_code}.png"
    img.save(filename)
    return filename, full_url
