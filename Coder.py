import os


def coder(header_name, name):
    # создадим переменные под исходный и конечный
    # размеры архива
    original_size = os.path.getsize(f"{header_name}")
    final_size = 0

    # создание нового файла и вставка в него заголовка
    new_file = open(name, "wb")
    with open(header_name, 'rb') as f:
        header = f.read()
    new_file.write(header)

    for root, dirs, files in os.walk("files"):
        # запись папок в архив
        for dirname in dirs:
            p = os.path.join(root, dirname)
            p = p.split('\\')
            p = p[-2] + '\\' + p[-1]
            pathsize = len(p)
            new_file.write(pathsize.to_bytes(4, byteorder='big', signed=False))
            new_file.write(bytes(p, encoding='utf-8'))
            original_size += pathsize

        # вставка файлов в архив
        for filename in files:
            # находим в каких каталогах находятся файлы
            # записываем в 'p' в виде folder\filename

            p = os.path.join(root, filename)
            # print(p)
            # при архивировании будем сначала выделять 8 байтов под размер самого файла
            # и 4 байта под размер имени файла + папки
            # затем со смещением 12 байт будет размещаться уже сам файл
            with open(p, 'rb') as f:
                filesize = os.path.getsize(p)
                new_file.write(filesize.to_bytes(8, byteorder='big', signed=False))
                p = p.split('\\')
                p = p[-2] + '\\' + p[-1]
                pathsize = len(p)
                new_file.write(pathsize.to_bytes(4, byteorder='big', signed=False))
                original_size += filesize + pathsize

                # print(p)
                new_file.write(bytes(p, encoding='utf-8'))
                new_file.write(f.read())

    # print(original_size)
    # print(original_size.to_bytes(8, byteorder='big', signed=False))
    # запишем размеры архива в header
    # исходный
    new_file.seek(12, 0)
    new_file.write(original_size.to_bytes(8, byteorder='big', signed=False))
    # конечный
    # new_file.seek(20, 0)
    new_file.write(original_size.to_bytes(8, byteorder='big', signed=False))


if __name__ == '__main__':
    coder('header0', 'archive')
