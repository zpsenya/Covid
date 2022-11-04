import qrcode


def qr_code_generation(client_name, client_surname):
    img = qrcode.make(f"{client_name}_{client_surname}")
    img.save('static/qr.png')
    return img
