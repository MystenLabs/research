import csv
import math
import matplotlib.pyplot as plt

# Initialize the cache with factorials for n = 0 and n = 1
factorials = [1, 1]
threshold = 2 ** 128
max_n = 10000


def factorial(n):
    """
    Computes the factorial of a non-negative integer n.

    Args:
        n: The non-negative integer to compute the factorial of.

    Returns:
        The factorial of n.
    """
    # Check if the factorial is already in the cache
    if n < len(factorials):
        return factorials[n]

    # Compute and cache the factorial
    result = factorials[-1]
    for i in range(len(factorials), n + 1):
        result *= i
        factorials.append(result)
    return result


def compute_combinations(n):
    """
    Computes various properties of the binomial coefficient C(n, k) for n.

    Args:
        n: The integer to compute the properties for.

    Returns:
        A tuple containing:
        - n: The integer passed as an argument.
        - min_k_for_aggregated_combinations: The minimum value of k such that
          the sum of C(n, k) for k in the range [0, k_min] is less than or equal
          to 2**128.
        - log_sum_of_combinations_min_k_aggregated_combinations: The base-2 logarithm of the sum of C(n, k)
          for k in the range [0, min_k_for_aggregated_combinations].
        - sum_of_combinations_min_k_aggregated_combinations: The integer value of the sum of C(n, k) for k
          in the range [0, min_k_for_aggregated_combinations].
        - min_k: The largest integer value of k that we can tolerate such that C(n, min_k) < threshold.
        - log_combinations_min_k: The base-2 logarithm of C(n, min_k).
        - combinations_min_k: The integer value of C(n, min_k).
        - max_k: The first integer where C(n, max_k) > threshold.
        - log_combinations_max_k: The base-2 logarithm of C(n, max_k).
        - combinations_max_k: The integer value of C(n, max_k).
    """
    # Compute the minimum value of k for which the aggregated number of combinations is less than 2^128
    sum_of_combinations_min_k_aggregated_combinations = 0
    min_k_for_aggregated_combinations = n
    for k in range(1, n + 1):
        combinations_k = factorial(n) // (factorial(k) * factorial(n - k))
        sum_of_combinations_min_k_aggregated_combinations += combinations_k
        if sum_of_combinations_min_k_aggregated_combinations > 2 ** 128:
            # We found a k that surpasses the threshold, so we subtract last combination addition
            min_k_for_aggregated_combinations = k - 1
            sum_of_combinations_min_k_aggregated_combinations -= combinations_k
            break
    log_sum_of_combinations_min_k_aggregated_combinations = math.log2(sum_of_combinations_min_k_aggregated_combinations)

    # Compute the first value of k C(n, k) > threshold
    combinations_max_k = 0
    max_k = n
    for k in range(min_k_for_aggregated_combinations, n + 1):
        combinations_max_k = factorial(n) // (factorial(k) * factorial(n - k))
        if combinations_max_k > threshold:
            max_k = k
            break
    log_combinations_max_k = math.log2(combinations_max_k)

    # Compute the largest integer value of k that we can tolerate such that C(n, k) < threshold
    min_k = max_k - 1
    if combinations_max_k > threshold:
        combinations_min_k = factorial(n) // (factorial(min_k) * factorial(n - min_k))
    else:
        min_k = max_k
        combinations_min_k = combinations_max_k
    log_combinations_min_k = math.log2(combinations_min_k)

    return n, \
        min_k_for_aggregated_combinations, \
        log_sum_of_combinations_min_k_aggregated_combinations, \
        sum_of_combinations_min_k_aggregated_combinations, \
        min_k, \
        log_combinations_min_k, \
        combinations_min_k, \
        max_k, \
        log_combinations_max_k, \
        combinations_max_k


def main_write_to_scv():
    # Open the CSV file for writing
    with open('combinations.csv', mode='w', newline='') as csv_file:
        # Create the CSV writer object
        writer = csv.writer(csv_file)

        # Write the header row to the CSV file
        writer.writerow(['n',
                         'min_k_for_aggregated_combinations',
                         'log_sum_of_combinations_min_k_aggregated_combinations',
                         'sum_of_combinations_min_k_aggregated_combinations',
                         'min_k',
                         'log_combinations_min_k',
                         'combinations_min_k',
                         'max_k',
                         'log_combinations_max_k',
                         'combinations_max_k'])

        # Find the minimum value of k for each value of n up to 1 million
        for n in range(1, max_n + 1):
            n, \
                min_k_for_aggregated_combinations, \
                log_sum_of_combinations_min_k_aggregated_combinations, \
                sum_of_combinations_min_k_aggregated_combinations, \
                min_k, \
                log_combinations_min_k, \
                combinations_min_k, \
                max_k, \
                log_combinations_max_k, \
                combinations_max_k = compute_combinations(n)

            writer.writerow([n,
                             min_k_for_aggregated_combinations,
                             log_sum_of_combinations_min_k_aggregated_combinations,
                             sum_of_combinations_min_k_aggregated_combinations,
                             min_k,
                             log_combinations_min_k,
                             combinations_min_k,
                             max_k,
                             log_combinations_max_k,
                             combinations_max_k])
            if n % 1_000 == 0:
                print(f"Processed {n} values of n")
    print("Done.")


def main_print_only():
    print("Starting...")
    # Find the minimum value of k for each value of n up to 1 million
    for n in range(1, max_n + 1):
        n, \
            min_k_for_aggregated_combinations, \
            log_sum_of_combinations_min_k_aggregated_combinations, \
            sum_of_combinations_min_k_aggregated_combinations, \
            min_k, \
            log_combinations_min_k, \
            combinations_min_k, \
            max_k, \
            log_combinations_max_k, \
            combinations_max_k = compute_combinations(n)
        print(f"{n},"
              f"{min_k_for_aggregated_combinations},"
              f"{log_sum_of_combinations_min_k_aggregated_combinations},"
              f"{sum_of_combinations_min_k_aggregated_combinations},"
              f"{min_k},{log_combinations_min_k},"
              f"{combinations_min_k},"
              f"{max_k},"
              f"{log_combinations_max_k},"
              f"{combinations_max_k}")


def plot_csv():
    # Extract the data from the CSV file
    with open('combinations.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the header row
        next(reader)
        data = [(int(row[0]), int(row[1])) for row in reader]

    # create a plot for the n <= 300
    # Filter data for n <= 300
    data = [(n, min_k) for n, min_k in data if n <= 300]

    x = [row[0] for row in data]
    y = [row[1] for row in data]
    plt.plot(x, y, linewidth=1.5)

    # Set x-axis ticks and tick labels
    x_tick_labels = ['{:,}'.format(i) for i in range(0, max(x) + 1, 10)]
    plt.xticks(range(0, max(x) + 1, 10), x_tick_labels)

    # Set y-axis ticks and tick labels
    plt.yticks(range(0, max(y) + 1, 5))

    # Display the values of min_k_for_aggregated_combinations for every 10
    for i in range(1, max(x) + 1, 10):
        index = x.index(i)
        plt.annotate(y[index], (x[index], y[index]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('n')
    plt.ylabel('max_k_aggregated_sum')
    plt.show()


if __name__ == '__main__':
    main_write_to_scv()
    plot_csv()
