import os
import sys


def get_header(version: int = 1, sub_version: int = 1):#, ctx: int = 0, no_ctx: int = 0, cypher: int = 0):
    header = bytes("BRIGADE7", encoding='ascii') + version.to_bytes(2, byteorder='big', signed=False) + \
             sub_version.to_bytes(2, byteorder='big', signed=False)
    return header


def coder(name, src_folder):
    # создадим переменные под исходный и конечный
    # размеры архива
    header_size = 64
    original_size = 64
    final_size = 0

    # создание нового файла и вставка в него заголовка
    try:
        new_file = open(name, "wb")
    except OSError as e:
        print(str(e) + "\n" + "Couldn't open file")
        return
    header = get_header(version=1, sub_version=0)
    new_file.write(header)
    new_file.seek(header_size)

    for root, dirs, files in os.walk(src_folder):
        # вставка файлов в архив
        for filename in files:
            # new_file.write(True.to_bytes(1, 'big'))
            new_file.write(bytes("B7", encoding='ascii'))
            # находим в каких каталогах находятся файлы
            # записываем в 'p' в виде folder\filename
            p = os.path.join(root, filename).replace('\\', '/')
            # при архивировании будем сначала выделять 8 байтов под размер самого файла
            # и 4 байта под размер имени файла + папки
            # затем со смещением 12 байт будет размещаться уже сам файл
            with open(p, 'rb') as f:
                filesize = os.path.getsize(p)
                new_file.write(filesize.to_bytes(8, byteorder='big', signed=False))
                # перекодирование строки в utf-8
                pathsize = len(p.encode(encoding='utf-8'))
                new_file.write(pathsize.to_bytes(4, byteorder='big', signed=False))
                original_size += filesize + pathsize
                new_file.write(bytes(p, encoding='utf-8'))
                new_file.write(f.read())

    # запишем размеры архива в header
    # исходный
    new_file.seek(12, 0)
    new_file.write(original_size.to_bytes(8, byteorder='big', signed=False))
    # конечный
    new_file.write(original_size.to_bytes(8, byteorder='big', signed=False))
    new_file.close()


if __name__ == '__main__':
    coder('archive', 'files')