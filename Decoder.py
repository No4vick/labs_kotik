import os


def decoder(header_name, archive_name):
    signature = ''
    header_size = os.path.getsize(header_name)

    #считаем сигнатуру и размер header
    with open(header_name, 'rb') as header:
        signature = header.read(8).decode(encoding='utf-8')

    print(signature)
    #разбираем header в архиве
    with open(archive_name, 'rb') as archive:
        #проверка сигнатуры
        if signature == archive.read(8).decode(encoding='utf-8'):
        #проверка кодов алгоритмов
            archive.seek(28, 0)
            with_context = int.from_bytes(archive.read(1), 'big')
            without_context = int.from_bytes(archive.read(1), 'big')
            print(with_context)
            print(without_context)
            if with_context == 0 and without_context == 0:
                os.mkdir('files_unpacked')
                print('поехали')
        else:
            print('неверный формат файла')



if __name__ == '__main__':
    decoder('header0', 'archive')
