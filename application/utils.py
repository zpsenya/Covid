import qrcode


def qr_code_generation(client_name, client_surname):
    qr = qrcode.QRCode(version=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=2, border=3)
    qr.add_data(f"{client_name}_{client_surname}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/qr.png')
    return img
