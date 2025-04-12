import os
import sys
import shutil
import pytest

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def get_results_dirs():
    """Get all results directories in the tests folder."""
    results_dirs = []
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
        if 'results' in dirs:
            results_dirs.append(os.path.join(root, 'results'))
    return results_dirs

@pytest.fixture(autouse=True, scope="session")
def cleanup_results_dirs():
    """Clean up all results directories before running tests."""
    results_dirs = get_results_dirs()
    for results_dir in results_dirs:
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)
        os.makedirs(results_dir)
    yield 