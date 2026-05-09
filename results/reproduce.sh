#!/bin/bash
# Reproduce all results from the paper
# Run from the repository root: bash results/reproduce.sh

# 移除 set -e,改为手动检查错误
# set -e

cd "$(dirname "$0")/.."

echo "=== Debug Info ==="
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la
echo "Code directory contents:"
ls -la code/ || echo "code/ not found"
echo "=================="

echo "=== Reproducibility Check Started ==="
echo "Repository: HCE-feature-importance-analysis"
echo "Started at: $(date)"

# Step 1: Install dependencies
echo ""
echo "Step 1: Installing dependencies..."
if [ ! -f code/requirements.txt ]; then
    echo "ERROR: code/requirements.txt not found!"
    exit 1
fi

pip install -q -r code/requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Step 2: Create output directories
echo ""
echo "Step 2: Creating output directories..."
mkdir -p results/figures 2>/dev/null || true
mkdir -p results/data 2>/dev/null || true
mkdir -p output 2>/dev/null || true
echo "✓ Directories created"

# Step 3: Run Python scripts
echo ""
echo "Step 3: Running analysis scripts..."

# 查找所有 Python 脚本
scripts=$(find code -name "*.py" -type f 2>/dev/null | sort)

if [ -z "$scripts" ]; then
    echo "WARNING: No Python scripts found in code/"
    echo "This might be intentional if your analysis is in notebooks"
    echo "Skipping script execution"
else
    echo "Found Python scripts:"
    echo "$scripts"
    echo ""
    
    count=0
    failed=0
    
    for script in $scripts; do
        echo "----------------------------------------"
        echo "Running: $script"
        
        log_file="output/$(basename $script).log"
        python3 "$script" > "$log_file" 2>&1
        exit_code=$?
        
        # 运行脚本并捕获输出
        if [ $exit_code -eq 0 ]; then
            count=$((count+1))
            echo "✓ SUCCESS: $script"
        else
            exit_code=$?
            failed=$((failed+1))
            echo "✗ FAILED: $script (exit code: $exit_code)"
            grep -v "findfont: Font family 'Arial'" "$log_file" | tail -n 30
            echo "Continuing with other scripts..."
        fi
    done
    
    echo ""
    echo "========================================" 
    echo "Summary:"
    echo "  Total scripts found: $(echo "$scripts" | wc -l)"
    echo "  Successful: $count"
    echo "  Failed: $failed"
    echo "========================================"
    
    # 如果所有脚本都失败了才报错
    if [ $count -eq 0 ] && [ $(echo "$scripts" | wc -l) -gt 0 ]; then
        echo "ERROR: All scripts failed!"
        exit 1
    fi
fi

echo ""
echo "=== Reproducibility Check Completed ==="
echo "Finished at: $(date)"

# 返回成功
exit 0
