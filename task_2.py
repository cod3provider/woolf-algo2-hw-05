import json
import time
from hyperloglog import HyperLogLog


def load_ip_addresses(filename):
    ip_addresses = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                if 'remote_addr' in log_entry:
                    ip_addresses.append(log_entry['remote_addr'])
            except json.JSONDecodeError:
                continue
    return ip_addresses


def count_unique_ips_set(ip_addresses):
    return len(set(ip_addresses))


def count_unique_ips_hll(ip_addresses, precision=0.01):
    hll = HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def main():
    filename = 'lms-stage-access.log'
    ip_addresses = load_ip_addresses(filename)

    start_time = time.time()
    exact_count = count_unique_ips_set(ip_addresses)
    exact_time = time.time() - start_time

    start_time = time.time()
    hyper_log_log_count = count_unique_ips_hll(ip_addresses)
    hyper_log_log_time = time.time() - start_time

    print("Результати порівняння:")
    print(f"{'':20}Точний підрахунок   HyperLogLog")
    print(f"{'Унікальні елементи':20}{exact_count:<15.1f}{hyper_log_log_count:<15.1f}")
    print(f"{'Час виконання (сек.)':20}{exact_time:<15.3f}{hyper_log_log_time:<15.3f}")
    print(f"Завантажено IP-адрес: {len(ip_addresses)}")


if __name__ == '__main__':
    main()
