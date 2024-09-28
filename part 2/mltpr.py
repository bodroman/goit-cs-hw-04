import os
import threading
import time
from queue import Queue

# Функція для пошуку ключових слів у файлах
def search_files(files, keywords, result_queue):
    result = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"Reading file {file}...")
                for keyword in keywords:
                    if keyword in content:
                        print(f"Keyword '{keyword}' found in {file}")
                        result[keyword].append(file)
                    else:
                        print(f"Keyword '{keyword}' not found in {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    result_queue.put(result)

# Основна функція для багатопотокової обробки файлів
def multithreaded_file_processing(file_list, keywords, num_threads=4):
    result_queue = Queue()
    threads = []
    chunk_size = len(file_list) // num_threads
    start_time = time.time()

    for i in range(num_threads):
        files_chunk = file_list[i*chunk_size:(i+1)*chunk_size]
        print(f"Thread {i} processing files: {files_chunk}")
        t = threading.Thread(target=search_files, args=(files_chunk, keywords, result_queue))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Збираємо результати
    final_result = {keyword: [] for keyword in keywords}
    while not result_queue.empty():
        result = result_queue.get()
        for keyword in keywords:
            final_result[keyword].extend(result[keyword])

    end_time = time.time()
    print(f"Multithreaded execution time: {end_time - start_time:.2f} seconds")
    return final_result

# Текст для файлів
file_contents = [
    "This is a test file containing keyword1.",
    "This file contains keyword2 and some additional text.",
    "Here we have both keyword1 and keyword2 in the same file.",
    "No keywords here, just some random content."
]

# Шляхи до файлів
file_paths = [
    r"C:\Users\roman\Reps\goit-cs-hw-04\file1.txt",
    r"C:\Users\roman\Reps\goit-cs-hw-04\file2.txt",
    r"C:\Users\roman\Reps\goit-cs-hw-04\file3.txt",
    r"C:\Users\roman\Reps\goit-cs-hw-04\file4.txt"
]

# Створюємо та записуємо файли з кодуванням utf-8
for i, content in enumerate(file_contents):
    try:
        with open(file_paths[i], 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"File {file_paths[i]} created successfully with UTF-8 encoding.")
    except Exception as e:
        print(f"Error writing to file {file_paths[i]}: {e}")

# Пошукові ключові слова
keywords = ["keyword1", "keyword2"]

# Запуск багатопотокової обробки файлів
result = multithreaded_file_processing(file_paths, keywords)
print(result)

