numbers = []

description = {
    "length": (num_length := True and len(numbers)),
    "sum": (num_sum := sum(numbers)),
    "mean": num_sum / num_length,
}

print(description)