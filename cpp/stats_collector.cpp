#include <llvm/IR/PassManager.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/Support/CommandLine.h>
#include <llvm/Support/JSON.h>
#include <llvm/Support/raw_ostream.h>
#include <llvm/IR/InstIterator.h>
#include <fstream>
#include <map>

using namespace llvm;

// Command line option to specify where to dump the JSON
static cl::opt<std::string> OutputFilename(
    "stats-json-out", 
    cl::desc("Output file for analysis statistics"), 
    cl::value_desc("filename"), 
    cl::init("stats.json"));

struct StatsCollector : public PassInfoMixin<StatsCollector> {
    
    // Store stats: Function Name -> {Stat Name -> Count}
    std::map<std::string, std::map<std::string, int>> FuncStats;

    PreservedAnalyses run(Module &M, ModuleAnalysisManager &) {
        
        for (Function &F : M) {
            if (F.isDeclaration()) continue;
            
            std::string FName = F.getName().str();
            int basicBlocks = 0;
            int memoryOps = 0;
            int callSites = 0;
            
            // "Program Analysis" Logic
            for (BasicBlock &BB : F) {
                basicBlocks++;
                for (Instruction &I : BB) {
                    if (isa<LoadInst>(I) || isa<StoreInst>(I)) {
                        memoryOps++;
                    }
                    if (isa<CallInst>(I) || isa<InvokeInst>(I)) {
                        callSites++;
                    }
                }
            }

            FuncStats[FName]["basic_blocks"] = basicBlocks;
            FuncStats[FName]["memory_ops"] = memoryOps;
            FuncStats[FName]["call_sites"] = callSites;
        }

        dumpToJSON();
        return PreservedAnalyses::all();
    }

    void dumpToJSON() {
        if (OutputFilename.empty()) return;

        // Manually build JSON string (simplest without extra dependencies)
        std::string jsonStr = "{\n";
        bool firstF = true;
        
        for (auto const & [func, stats] : FuncStats) {
            if (!firstF) jsonStr += ",\n";
            jsonStr += "  \"" + func + "\": {";
            
            bool firstS = true;
            for (auto const & [key, val] : stats) {
                if (!firstS) jsonStr += ", ";
                jsonStr += "\"" + key + "\": " + std::to_string(val);
                firstS = false;
            }
            jsonStr += "}";
            firstF = false;
        }
        jsonStr += "\n}\n";

        // Write to file accessible by Python
        std::ofstream OutFile(OutputFilename);
        OutFile << jsonStr;
        OutFile.close();
    }
};

// Plugin Entry Point
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {LLVM_PLUGIN_API_VERSION, "StatsCollector", "v0.1",
            [](PassBuilder &PB) {
                PB.registerPipelineParsingCallback(
                    [](StringRef Name, ModulePassManager &MPM,
                       ArrayRef<PassBuilder::PipelineElement>) {
                        if (Name == "collect-stats") {
                            MPM.addPass(StatsCollector());
                            return true;
                        }
                        return false;
                    });
            }};
}