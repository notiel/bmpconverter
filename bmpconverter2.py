from PIL import Image
import time
import serial
import sys, os


def main(folder: str, comport: str, delay: int, depth: int):
    try:
        ser = serial.Serial(comport, baudrate=115200)
    except Exception:
        print("COM-порт недоступен")
        return

    while True:
        for file in os.listdir(folder):
            if '.' in file and file.split('.')[1].lower() == 'bmp':
                data = Image.open(folder+'\\'+file)
                pixels = data.getdata()
                command = bytes()
                for i in range (data.size[1]):
                    for j in range(data.size[0]):
                        r, g, b = pixels[i*data.size[0] + j]
                        #print(r, g, b)
                        if depth != 8:
                            r = r >> (8 - depth)
                            g = g >> (8 - depth)
                            b = b >> (8 - depth)
                        command += r.to_bytes(1, byteorder='big')
                        command += g.to_bytes(1, byteorder='big')
                        command += b.to_bytes(1, byteorder='big')

                ser.write(command)
                #print(command)
                time.sleep(0.001*delay)
    # ser.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Недостаточно параметров, ожидаемыее параметры: имя папки, номер компорта, таймаут в мс, глубина цвета")
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))