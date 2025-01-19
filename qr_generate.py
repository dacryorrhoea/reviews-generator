import qrcode

data = """
"""

# Создание QR-кода
qr = qrcode.QRCode(
    version=1,  # Размер QR-кода (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
    box_size=10,  # Размер каждой "клетки" QR-кода
    border=1,  # Ширина границы
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# Сохранение изображения
img.save("qrcode.png")