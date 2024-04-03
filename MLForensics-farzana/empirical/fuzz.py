import random
import time
import csv
import os

from report import giveTimeStamp, Average, Median, reportProp, reportDensity

# Define the methods to fuzz
methods_to_fuzz = [giveTimeStamp, Average, Median, reportProp, reportDensity]

# Define the fuzzing parameters
num_iterations = 5


# Function to create dummy CSV files with random data
def create_dummy_files():
    field_names = ['CATEGORY', 'PROP_VAL', 'EVENT_DENSITY']
    categories = ['DATA_LOAD_COUNT', 'MODEL_LOAD_COUNT', 'DATA_DOWNLOAD_COUNT',
                  'MODEL_LABEL_COUNT', 'MODEL_OUTPUT_COUNT', 'DATA_PIPELINE_COUNT',
                  'ENVIRONMENT_COUNT', 'STATE_OBSERVE_COUNT', 'TOTAL_EVENT_COUNT']
    created_files = []

    for category in categories:
        file_name = f"{random.choice(['PROPORTION', 'DENSITY'])}_{category}.csv"
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            # Generate a non-zero proportion value between 0.1 and 1
            prop_val = random.uniform(0.1, 1)
            # Generate a non-zero event density between 0 and 100
            event_density = random.uniform(1, 100)
            writer.writerow({'CATEGORY': category, 'PROP_VAL': prop_val, 'EVENT_DENSITY': event_density})
        print(f"Dummy CSV file created: {file_name}")
        created_files.append(file_name)
    return created_files


# Fuzz the methods
def fuzz_methods():
    # Create dummy files before fuzzing
    created_files = create_dummy_files()

    for method in methods_to_fuzz:
        for _ in range(num_iterations):
            try:
                # Generate random inputs or use semi-random strategies
                if method == giveTimeStamp:
                    # No input required for giveTimeStamp
                    wait_time = random.uniform(0, 3)  # Random wait time between 0 and 3 seconds
                    time.sleep(wait_time)
                    random_input = ()
                elif method == Average or method == Median:
                    # Generate a random list of integers for Average and Median
                    random_input = (random.choices(range(1, 100), k=random.randint(1, 10)),)
                elif method == reportProp or method == reportDensity:
                    # For reportProp and reportDensity, might need a file name as input
                    random_file = random.choice(created_files)
                    random_input = (random_file,)
                else:
                    # For other methods, no additional inputs are needed
                    random_input = ()

                # Call the method with the generated input
                output = method(*random_input)

                # Print both the input and output
                print(f"Input for {method.__name__}: {random_input}")
                print(f"Output for {method.__name__}: {output}")
            except Exception as e:
                # Log any exceptions or errors raised during fuzzing
                print(f"Bug discovered in {method.__name__}: {e}")

    # Cleanup: Delete the dummy files
    for file_name in created_files:
        os.remove(file_name)
        print(f"Dummy CSV file deleted: {file_name}")


# Execute fuzzing
fuzz_methods()
