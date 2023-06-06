import pandas as pd
import zipfile
import os
import sys
import tempfile
import shutil


# директория данных
dir_data = '/data'
# получаем урл из входных аргументов
gtfs_url = str(sys.argv[1])
# извлекаем из него имя архива с которым работаем
archive = gtfs_url.split("/")[-1]

# Загрузим route_types_mapping.csv в датафрейм pandas
mapping_df = pd.read_csv('route_types_mapping.csv')

# зададим функцию удаления файла из архива
def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)

# сменяем текущую директорию на директорию данных
os.chdir(dir_data)

# извлечем файл routes.txt'
with zipfile.ZipFile(archive, 'r') as zip_file:
    zip_file.extract('routes.txt')

# Загрузим routes.txt в датафрейм pandas
routes_df = pd.read_csv('routes.txt')

# Замена неподдерживаемых типов маршрутов поддерживаемыми с помощью сопоставления
routes_df['route_type'].replace(dict(zip(mapping_df['route_type_in'], mapping_df['route_type_out'])), inplace=True)

# сохраним результат в  routes.txt
routes_df.to_csv('routes.txt', index=False)

# Удаляем файл routes.txt из исходного архива
remove_from_zip(archive, 'routes.txt')

# Добавим файл routes.txt в исходный архив
with zipfile.ZipFile(archive, 'a') as z:
    z.write('routes.txt')

os.remove('routes.txt')
