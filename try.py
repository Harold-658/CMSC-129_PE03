def is_sequence_starting_from_one(arr):
    # Convert array elements to integers
    arr = [int(x) for x in arr]
    
    # Check if the array is a sequence starting from 1
    if arr[0] != 1:
        return False

    for i in range(len(arr) - 1):
        if arr[i] + 1 != arr[i + 1]:
            return False
    return True

# Example usage:
correct_sequence = ['1', '3', '2', '4', '5']
incorrect_sequence = ['1', '3', '4', '5', '6']

result_correct = is_sequence_starting_from_one(correct_sequence)
result_incorrect = is_sequence_starting_from_one(incorrect_sequence)

print("Correct Sequence:", result_correct)
print("Incorrect Sequence:", result_incorrect)
