import socket
import json
import qrcode
from PIL import Image, ImageDraw, ImageFont

PRINTER_IP = "192.168.1.15"
PRINTER_PORT = 9100

DPI = 300
TAPE_WIDTH_MM = 36
TAPE_WIDTH_PX = int(TAPE_WIDTH_MM / 25.4 * DPI)

def create_label(qr_text, part_no):
    qr = qrcode.QRCode(box_size=6, border=1)
    qr.add_data(qr_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    height = max(qr_img.height + 40, 300)
    label = Image.new("RGB", (TAPE_WIDTH_PX, height), "white")
    label.paste(qr_img, (20, 20))

    draw = ImageDraw.Draw(label)
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((qr_img.width + 40, 120), part_no, fill="black", font=font)

    return label

def escp_raster(img):
    bw = img.convert("1")
    width_bytes = (bw.width + 7) // 8
    data = bw.tobytes()

    cmd = bytearray()
    cmd += b'\x1b\x40'          # 初期化
    cmd += b'\x1b\x69\x61\x01'  # 自動カットON
    cmd += b'\x1b\x69\x4d\x40'  # 36mm

    offset = 0
    for _ in range(bw.height):
        cmd += b'\x67\x00'
        cmd += width_bytes.to_bytes(2, 'little')
        cmd += data[offset:offset + width_bytes]
        offset += width_bytes

    cmd += b'\x1a'  # 印刷
    return cmd

def send_to_printer(data):
    with socket.create_connection((PRINTER_IP, PRINTER_PORT)) as s:
        s.sendall(data)

def load_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- メイン処理 ----------
items = load_from_json("labels.json")

for item in items:
    qr = item["qr"]
    part_no = item["part_no"]

    label_img = create_label(qr, part_no)
    escp = escp_raster(label_img)
    send_to_printer(escp)