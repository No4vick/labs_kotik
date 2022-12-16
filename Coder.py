import os
import Compressor as cr


def get_header(version: int = 1, sub_version: int = 1, ctx: int = 0, no_ctx: int = 0, cypher: int = 0,
               start_size: int = 0, final_size: int = 0):
    header = bytes("BRIGADE7", encoding='ascii') + version.to_bytes(2, byteorder='big', signed=False) + \
             sub_version.to_bytes(2, byteorder='big', signed=False) + start_size.to_bytes(8, byteorder='big',
                                                                                      signed=False) + \
             final_size.to_bytes(8, byteorder='big', signed=False) + ctx.to_bytes(1, byteorder='big', signed=False) + \
             no_ctx.to_bytes(1, byteorder='big', signed=False) + cypher.to_bytes(1, byteorder='big', signed=False)
    return header


def get_option_bytes(option: int | list, count: int = None) -> bytes:
    if type(option) is list and count is not None:
        return option[count].to_bytes(1, byteorder='big', signed=False)
    else:
        return option.to_bytes(1, byteorder='big', signed=False)


def get_option(option: int | list, count: int = None) -> int:
    if type(option) is list and count is not None:
        return option[count]
    else:
        return option


def file_coder(file_full: bytes, filecount: int, p: str, nctx_compression: int | list, ctx_compression: int | list = 0, cypher: int | list = 0) -> tuple:
    file_header = 0
    filename = p[p.rfind('/') + 1:]
    filesize = os.path.getsize(p)
    # new_file.write(filesize.to_bytes(8, byteorder='big', signed=False))
    file_header = filesize.to_bytes(8, byteorder='big', signed=False)
    # original_size += filesize
    original_filesize = filesize
    # всякие преобразования в файле
    file_ctx_compressed = cr.ctx_compress(file_full, get_option(ctx_compression, filecount))
    file, nctx_dict = cr.nctx_compress(file_ctx_compressed, get_option(nctx_compression, filecount))
    # проверка целесообразности сжатия
    n = filesize
    # is_useless = True
    if get_option(nctx_compression, filecount) != 0:
        n_comp = len(file) + len(nctx_dict) + 2
        is_useless = n <= n_comp
        if is_useless:
            print(f"compression is useless for {filename} :")
            print(f"n = {n} , n_comp = {n_comp}")
            # print(filecount)
            nctx_compression[filecount] = 0
            file = file_full

    file = cr.cypher(file, get_option(cypher))
    # записываем финальный размер
    # new_file.write(len(file).to_bytes(8, byteorder='big', signed=False))
    file_header += len(file).to_bytes(8, byteorder='big', signed=False)
    # запись сжатий и шифрования
    # new_file.write(get_option_bytes(ctx_compression, filecount))
    file_header += get_option_bytes(ctx_compression, filecount)
    # new_file.write(get_option_bytes(nctx_compression, filecount))
    file_header += get_option_bytes(nctx_compression, filecount)
    # new_file.write(get_option_bytes(cypher, filecount))
    file_header += get_option_bytes(cypher, filecount)
    # перекодирование строки в utf-8
    pathsize = len(p.encode(encoding='utf-8'))
    # запись пути к файлу
    # new_file.write(pathsize.to_bytes(4, byteorder='big', signed=False))
    file_header += pathsize.to_bytes(4, byteorder='big', signed=False)
    # final_size += filesize + pathsize
    final_filesize = filesize + pathsize
    # original_size += pathsize
    original_filesize += pathsize
    # запись имени файла
    # new_file.write(bytes(p, encoding='utf-8'))
    file_header += bytes(p, encoding='utf-8')
    if get_option(nctx_compression, filecount) != 0:
        # запись Длины словаря кодировки без контекста
        # new_file.write(bytes(len(nctx_dict)))
        # new_file.write(len(nctx_dict).to_bytes(2, byteorder='big'))
        file_header += len(nctx_dict).to_bytes(2, byteorder='big')
        # запись словаря кодировки без контекста
        # print(f"len nctx_dict = {len(nctx_dict)}")
        # new_file.write(nctx_dict)
        file_header += nctx_dict
    if get_option(ctx_compression) != 0:
        # запись Длины словаря кодировки с контекстом
        # запись словаря кодировки c контекстом
        pass
    # запись файла
    file = file_header + file
    return file, original_filesize, final_filesize


def coder(name, src_folder, nctx_compression: int | list, ctx_compression: int | list = 0, cypher: int | list = 0, whole: int = 0):
    """

    :param cypher:
    :param ctx_compression:
    :param name:
    :param src_folder:
    :param nctx_compression: Тип(ы) сжатия без контекста: 0 - нет, 1 - Шеннон, 2 - Шеннон-Фано, 3 - Хаффман
    :param whole: Кодирование файловой структуры как одного файла : 0 - нет: 1 - да.
    :return:
    """
    # создадим переменные под исходный и конечный
    # размеры архива
    header_size = 64
    original_size = 64
    final_size = 64

    # создание нового файла и вставка в него заголовка
    try:
        new_file = open(name, "wb")
    except OSError as e:
        print(str(e) + "\n" + "Couldn't open file")
        return
    header = get_header(version=1, sub_version=0)
    new_file.write(header)
    new_file.seek(header_size)
    filecount = 0
    for root, dirs, files in os.walk(src_folder):

        # if type(nctx_compression) is list and len(nctx_compression) != len(files):
        #     raise ValueError("A")
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
                file_full = f.read()
                file, original_filesize, final_filesize = file_coder(file_full, filecount, p, nctx_compression, ctx_compression, cypher)
                original_size += original_filesize
                final_size += final_filesize
                new_file.write(file)
            filecount += 1

    # запишем размеры архива в header
    # исходный
    new_file.seek(12, 0)
    new_file.write(original_size.to_bytes(8, byteorder='big', signed=False))
    # конечный
    new_file.write(final_size.to_bytes(8, byteorder='big', signed=False))
    new_file.close()


if __name__ == '__main__':
    coder('archive', 'files', [1, 1, 1, 1], 0, 0)
