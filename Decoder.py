import os
import Decompressor as dr


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
                original_size = int.from_bytes(archive.read(8), byteorder='big', signed=False)
                # Считывания обработки файла
                new_size = int.from_bytes(archive.read(8), byteorder='big', signed=False)
                ctx_compression = int.from_bytes(archive.read(1), byteorder='big', signed=False)
                nctx_compression = int.from_bytes(archive.read(1), byteorder='big', signed=False)
                cypher = int.from_bytes(archive.read(1), byteorder='big', signed=False)
                # Считывание размера пути
                path_size = int.from_bytes(archive.read(4), byteorder='big', signed=False)
                # Считывание и декодирование пути
                path = os.path.normpath(archive.read(path_size).decode(encoding='utf-8')).replace('\\', '/')
                # file = archive.read(new_size)
                # Развёртывание файла

                # Считывание длины словаря кодировки без контекста
                nctx_header_size = int.from_bytes(archive.read(2), byteorder='big')
                nctx_header = archive.read(nctx_header_size)
                # Считывание словаря кодировки без контекста
                # развертывание без контекста
                # print(nctx_header)
                file = archive.read(new_size)
                file = dr.nctx_decompress(file, nctx_header, nctx_compression)
                # Считывание длины словаря кодировки с контекстом
                # Считывание словаря кодировки с контекстом
                file = dr.ctx_decompress(file, ctx_compression)
                file = dr.decypher(file, cypher)
                if len(file) != original_size:
                    raise RuntimeError(f"OH no! len file {path} is {len(file)} but original size is {original_size}")
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
