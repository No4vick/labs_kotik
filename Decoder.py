import os


def decoder(archive_name):
    signature = ''
    header_size = 64

    # считаем сигнатуру и размер header
    signature = "BRIGADE7"

    # разбираем header в архиве
    with open(archive_name, 'rb') as archive:
        # проверка сигнатуры
        if signature == archive.read(8).decode(encoding='utf-8'):
            # проверка кодов алгоритмов
            archive.seek(28, 0)
            with_context = int.from_bytes(archive.read(1), 'big')
            without_context = int.from_bytes(archive.read(1), 'big')
            archive.seek(64)
            if archive.read(2) != b'B7':
                print('No files found')
                return
            while True:
                # Считывание размера файла и размера пути
                size = int.from_bytes(archive.read(8), byteorder='big', signed=False)
                path_size = int.from_bytes(archive.read(4), byteorder='big', signed=False)
                # Считывание и декодирование пути
                path = os.path.normpath(archive.read(path_size).decode(encoding='utf-8')).replace('\\', '/')
                file = archive.read(size)
                # Создание пути папок
                folder_path = path[:path.rfind('/')]
                os.makedirs(folder_path, exist_ok=True)
                # Запись файла
                with open(path, 'wb') as f:
                    f.write(file)
                # Если не нашлась следующая сигнатура выходим
                if archive.read(2) != b'B7':
                    break
        else:
            print('Неверный формат файла')


if __name__ == '__main__':
    decoder('archive')
