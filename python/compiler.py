# compiler.py
import subprocess
import os
import re
from dataclasses import dataclass

@dataclass
class IRStats:
    func_name: str
    basic_blocks: int
    branches: int
    memory_ops: int
    ir_content: str

class LLVMCompiler:
    def __init__(self):
        self.clang_cmd = "clang"

    def compile_to_ir(self, source_code: str, output_name: str) -> str:
        """Compiles C source to LLVM IR (.ll)"""
        src_file = f"{output_name}.c"
        ir_file = f"{output_name}.ll"
        
        with open(src_file, "w") as f:
            f.write(source_code)

        # -O1 is often better for analysis than O0 (less noise) but clearer than O3
        cmd = [self.clang_cmd, "-S", "-emit-llvm", "-O1", src_file, "-o", ir_file]
        subprocess.run(cmd, check=True)
        
        with open(ir_file, "r") as f:
            return f.read()

    def analyze_ir(self, ir_content: str) -> dict:
        """
        Regex-based Static Analysis. 
        In a real research job, you'd use 'llvmlite', but this is faster for a 12h project.
        """
        stats = {}
        # Simple heuristic to find function definitions
        funcs = re.split(r'define .* @(\w+)\(', ir_content)
        
        # Skip preamble
        for i in range(1, len(funcs), 2):
            fname = funcs[i]
            body = funcs[i+1]
            
            stats[fname] = {
                "basic_blocks": len(re.findall(r'\n\s*\w+:', body)) + 1, # Label counts
                "branches": body.count(" br "),
                "loads": body.count(" load "),
                "stores": body.count(" store "),
                "calls": body.count(" call "),
                "size_bytes": len(body)
            }
        return stats