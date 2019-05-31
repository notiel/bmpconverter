from PIL import Image
import time
import serial
import sys, os, json


def main(folder: str, comport: str, delay: int, depth: int):
    try:
        ser = serial.Serial(comport, baudrate=115200)
    except Exception:
        print("COM-порт недоступен")
        return

    try:
        while True:
            for file in os.listdir(folder):
                if file.lower().endswith('.bmp'):
                    data = Image.open(os.path.join(folder, file))
                    w, h = data.size
                    command = ":30"
                    for i in range (w):
                        for j in range(h):
                            r, g, b  = data.getpixel((i, j))
                            #print(r, g, b)
                            if depth != 8:
                                r = r >> (8 - depth)
                                g = g >> (8 - depth)
                                b = b >> (8 - depth)
                            command += r.to_bytes(1, byteorder='big').hex()
                            command += g.to_bytes(1, byteorder='big').hex()
                            command += b.to_bytes(1, byteorder='big').hex()

                    command+='\r\n'
                    ser.write(bytes(command, encoding='utf-8'))
                    print(command)
                    time.sleep(0.001*delay)
    finally:
        ser.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) >= 5:
            main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        else:
            print("Недостаточно параметров, ожидаемыее параметры: имя папки, номер компорта, таймаут в мс, глубина цвета")
    else:
        try:
            settings = json.load(open("Settings.json"))
            main(settings['Path'], settings['Port'], int(settings['Timeout_ms']), int(settings['Color_depth']))
        except (FileNotFoundError, FileExistsError, KeyError, json.decoder.JSONDecodeError):
            print("No file Settings.json or wrong file format")
            print(r'Expected format: {"Path": "somepath", "Port":"COMX", "Timeout_ms": timeout, "Color_depth": depth(1..8)')
