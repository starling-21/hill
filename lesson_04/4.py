import os
import time
import typing
from functools import wraps
from pathlib import Path

from pympler import asizeof

LESSON_04_ROOT = Path(__file__).parent
DATA_ROOT = Path.joinpath(LESSON_04_ROOT, "data")
FILTERED_DATA_PATH = Path.joinpath(DATA_ROOT, "filtered")
ROCKYOU_FILEPATH = Path.joinpath(LESSON_04_ROOT, "rockyou.txt")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time = end - start
        print(f"Function {func.__name__} took {total_time} seconds")
        return result

    return wrapper


def init_data_dirs():
    for path in [DATA_ROOT, FILTERED_DATA_PATH]:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)


def get_test_file_lines():
    data = []
    with open(ROCKYOU_FILEPATH, "r") as file:
        for line in file.readlines():
            data.append(line)
    return data


# Bad one
def generate_test_file_lines():
    with open(ROCKYOU_FILEPATH, "r") as file:
        for line in file.readlines():
            yield line


# Good one
def generate_test_file_lines_good():
    with open(ROCKYOU_FILEPATH, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line


@timeit
def filter_file_flow_write(pattern: str) -> typing.Dict[str, int]:
    result_filepath = f"{Path.joinpath(FILTERED_DATA_PATH, pattern)}.txt"
    lines_count = 0
    memory_size = 0

    with open(result_filepath, "w", encoding="UTF-8") as f:
        for line in generate_test_file_lines_good():
            if pattern in line.lower():
                f.write(line)
                lines_count += 1
                memory_size += asizeof.asizeof(line)

    result = {"total_size": os.path.getsize(result_filepath), "lines_count": lines_count, "memory_size": memory_size}
    return result


@timeit
def filter_file_buffered_flow_write(pattern: str) -> typing.Dict[str, int]:
    result_filepath = f"{Path.joinpath(FILTERED_DATA_PATH, pattern)}.txt"
    lines_count = 0
    memory_size = 0
    buffer = list()
    buffer_size = 100000

    with open(result_filepath, "w", encoding="UTF-8") as f:
        for line in generate_test_file_lines_good():
            if pattern in line.lower():
                buffer.append(line)
                lines_count += 1

            if len(buffer) > buffer_size:
                memory_size += asizeof.asizeof(buffer)
                f.writelines(buffer)
                del buffer[:]

    result = {"total_size": os.path.getsize(result_filepath), "lines_count": lines_count, "memory_size": memory_size}
    return result


@timeit
def filter_file_array_write(pattern: str) -> typing.Dict[str, int]:
    result_filepath = f"{Path.joinpath(FILTERED_DATA_PATH, pattern)}.txt"
    lines_count = 0
    memory_size = 0
    data = list()

    with open(result_filepath, "w", encoding="UTF-8") as f:
        for line in generate_test_file_lines_good():
            if pattern in line.lower():
                data.append(line)
                lines_count += 1

        f.writelines(data)
        memory_size = asizeof.asizeof(data)

    result = {"total_size": os.path.getsize(result_filepath), "lines_count": lines_count, "memory_size": memory_size}
    return result


def main():
    init_data_dirs()
    pattern = input("Enter search pattern:")
    filter_info = filter_file_flow_write(pattern)
    print(
        f'Lines matched: {filter_info.get("lines_count", 0)}\n'
        f'Total size in Bytes: {filter_info.get("total_size", 0)}\n'
        f'Memory used for filtered data in Bytes: {filter_info.get("memory_size", 0)}'
    )

    print("-------------------------------------------------")
    filter_info = filter_file_buffered_flow_write(pattern)
    print(
        f'Lines matched: {filter_info.get("lines_count", 0)}\n'
        f'Total size in Bytes: {filter_info.get("total_size", 0)}\n'
        f'Memory used for filtered data in Bytes: {filter_info.get("memory_size", 0)}'
    )

    print("-------------------------------------------------")
    filter_info = filter_file_array_write(pattern)
    print(
        f'Lines matched: {filter_info.get("lines_count", 0)}\n'
        f'Total size in Bytes: {filter_info.get("total_size", 0)}\n'
        f'Memory used for filtered data in Bytes: {filter_info.get("memory_size", 0)}'
    )


if __name__ == "__main__":
    main()
