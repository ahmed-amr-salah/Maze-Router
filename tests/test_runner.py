import os
import sys
import subprocess
from filecmp import cmp

# Add the project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
print(f"PYTHONPATH set to: {project_root}")

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = [line.strip() for line in f1.readlines()]  # Remove trailing whitespace
        lines2 = [line.strip() for line in f2.readlines()]  # Remove trailing whitespace
    
    return lines1 == lines2

def run_test(test_dir):
    input_file = os.path.join(test_dir, "input.txt")
    expected_output_file = os.path.join(test_dir, "expected_output.txt")
    actual_output_file = os.path.join(test_dir, "actual_output.txt")

    # Full path to main.py
    main_script = os.path.join(project_root, "src", "main.py")
    
    try:
        # Use python3 explicitly with the absolute path to main.py
        result = subprocess.run(
            ["python3", main_script, input_file, actual_output_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Test failed in {test_dir}. Error:\n{result.stderr}")
            return False

        # Compare outputs
        if compare_files(expected_output_file, actual_output_file):
            print(f"Test passed in {test_dir}.")
            return True
        else:
            print(f"Test failed in {test_dir}. Output mismatch.")
            # uncomment the following line to see the diff output, if desired
            #subprocess.run(["diff", "-u", expected_output_file, actual_output_file])
            return False

    except Exception as e:
        print(f"Error running test in {test_dir}: {e}")
        return False


if __name__ == "__main__":
    # Full path to the test cases directory
    test_cases_dir = os.path.join(os.path.dirname(__file__), "test_cases")
    all_tests_passed = True

    for test_case in os.listdir(test_cases_dir):
        test_dir = os.path.join(test_cases_dir, test_case)
        if os.path.isdir(test_dir):
            if not run_test(test_dir):
                all_tests_passed = False

    if all_tests_passed:
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed.")
        exit(1)
