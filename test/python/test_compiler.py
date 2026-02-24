import os
import re
# Assuming you saved the class from the previous step in compiler.py
from compiler import LLVMCompiler 

def test_compiler_logic():
    compiler = LLVMCompiler()
    
    # 1. Define the Source Code
    vuln_code = """
    #include <stdlib.h>
    void* allocate_array(int num_elements) {
        size_t size = num_elements * sizeof(int);
        return malloc(size);
    }
    """

    patch_code = """
    #include <stdlib.h>
    #include <stdint.h>
    void* allocate_array(int num_elements) {
        if (num_elements < 0 || num_elements > 2147483647 / 4) {
            return NULL; 
        }
        size_t size = num_elements * sizeof(int);
        return malloc(size);
    }
    """

    print("--- 1. Compiling Vulnerable Code ---")
    vuln_ir = compiler.compile_to_ir(vuln_code, "vuln_test")
    vuln_stats = compiler.analyze_ir(vuln_ir)
    print(f"Vuln Stats: {vuln_stats}")

    print("\n--- 2. Compiling Patched Code ---")
    patch_ir = compiler.compile_to_ir(patch_code, "patch_test")
    patch_stats = compiler.analyze_ir(patch_ir)
    print(f"Patch Stats: {patch_stats}")

    # --- THE VERIFICATION LOGIC ---
    print("\n--- 3. Running Heuristic Checks ---")
    
    # Check 1: Did the patch increase complexity?
    # The patch adds an 'if' statement, which compiles to a 'br' (branch) instruction
    # and splits the code into multiple Basic Blocks.
    
    # Note: 'allocate_array' is the function name we are analyzing
    vuln_func_stats = vuln_stats.get('allocate_array', {})
    patch_func_stats = patch_stats.get('allocate_array', {})

    if not vuln_func_stats or not patch_func_stats:
        print("FAIL: Could not parse function 'allocate_array' from IR.")
        return

    print(f"Branches (Vuln): {vuln_func_stats.get('branches', 0)}")
    print(f"Branches (Patch): {patch_func_stats.get('branches', 0)}")

    if patch_func_stats['branches'] > vuln_func_stats['branches']:
        print("SUCCESS: Patch introduced new control flow branches.")
    else:
        print("FAIL: Patch did not increase branch count. Compiler might have optimized it away.")

    if patch_func_stats['basic_blocks'] > vuln_func_stats['basic_blocks']:
        print("SUCCESS: Patch introduced new basic blocks.")
    else:
        print("FAIL: Basic block count did not increase.")

if __name__ == "__main__":
    test_compiler_logic()