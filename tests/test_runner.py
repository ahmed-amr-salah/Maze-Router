import os
import subprocess
from filecmp import cmp

# Add the project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__)) + "/../"
os.environ["PYTHONPATH"] = project_root

def run_test(test_dir):
    input_file = os.path.join(test_dir, "input.txt")
    expected_output_file = os.path.join(test_dir, "expected_output.txt")
    actual_output_file = os.path.join(test_dir, "actual_output.txt")
    
    # Use python3 explicitly
    try:
        result = subprocess.run(
            ["python3", "src/main.py", input_file, actual_output_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Test failed in {test_dir}. Error:\n{result.stderr}")
            return False
        
        # Compare outputs
        if cmp(expected_output_file, actual_output_file, shallow=False):
            print(f"Test passed in {test_dir}.")
            return True
        else:
            print(f"Test failed in {test_dir}. Output mismatch.")
            return False

    except Exception as e:
        print(f"Error running test in {test_dir}: {e}")
        return False


if __name__ == "__main__":
    test_cases_dir = "tests/test_cases"
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
