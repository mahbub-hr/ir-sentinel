# server.py
from mcp.server.fastmcp import FastMCP
from compiler import LLVMCompiler
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Initialize MCP Server
mcp = FastMCP("IR-Sentinel")
compiler = LLVMCompiler()

# Initialize LLM (Gemini Free Tier)
# Ensure GOOGLE_API_KEY is in .env
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

@mcp.tool()
def analyze_patch_security(vuln_code: str, patched_code: str) -> str:
    """
    Takes vulnerable C code and patched C code.
    Compiles both to LLVM IR.
    Returns an AI research analysis of whether the patch is effective at the IR level.
    """
    try:
        # 1. Compile & Analyze VULN
        vuln_ir = compiler.compile_to_ir(vuln_code, "vuln")
        vuln_stats = compiler.analyze_ir(vuln_ir)

        # 2. Compile & Analyze PATCH
        patch_ir = compiler.compile_to_ir(patched_code, "patch")
        patch_stats = compiler.analyze_ir(patch_ir)

        # 3. Construct Research Prompt
        prompt = f"""
        You are a Senior Compiler Security Researcher.
        I have compiled two versions of a C function to LLVM IR.
        
        --- METADATA ---
        Vulnerable Stats: {json.dumps(vuln_stats, indent=2)}
        Patched Stats: {json.dumps(patch_stats, indent=2)}
        
        --- VULNERABLE IR (Snippet) ---
        {vuln_ir[:2000]} ...
        
        --- PATCHED IR (Snippet) ---
        {patch_ir[:2000]} ...
        
        --- TASK ---
        1. Compare the Control Flow Graph (CFG) structure based on the stats (did branches increase?).
        2. Analyze the IR diff. Did the patch introduce a check (icmp) followed by a branch (br)?
        3. VERDICT: Is the patch robust, or could compiler optimizations (like undefined behavior) remove it?
        """
        
        # 4. Invoke LLM
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error during analysis: {str(e)}"

if __name__ == "__main__":
    mcp.run()