prompt to files/project structure
Build a llm agent that will mount the attack on a live  system
Recreate sean  healn zero  day bug using llvm ir or binary code -> binrec ->> ir.


First, try with recreating the bug with LLVM IR.

1. optimize_and_compare
   * What it does: Compiles the same C code at -O1 and -O3, runs your StatsCollector on both, and returns a comparison.
   * Why it's appealing: It shows you understand how compiler optimizations (like loop unrolling or inlining) actually change code metrics. Interviewers love seeing that you don't treat the compiler as a "black box."


  2. visualize_cfg
   * What it does: Uses opt -dot-cfg to generate a Graphviz DOT file of the function's Control Flow Graph.
   * Why it's appealing: It provides a visual layer to the analysis. You could even have the LLM "describe" the graph structure to the user.


  3. security_audit_metrics
   * What it does: Uses your Pandas logic to identify "Hotspots"—functions with high cyclomatic complexity (many basic blocks) combined with high memory operations (loads/stores).
   * Why it's appealing: It demonstrates "Data-Driven Security." Instead of just looking at code, you're using metrics to prioritize where a human (or an LLM) should look for bugs.


  4. check_optimization_hazard
   * What it does: Specifically looks for patterns where a security check (like if (ptr == NULL) return;) might be optimized away due to Undefined Behavior earlier in the IR.
   