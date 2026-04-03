#!/bin/bash
# Reproduce all results from the paper
# Run from the repository root: bash results/reproduce.sh
#
# Expected runtime: [document here]
# Random seeds: [document here if applicable]

set -e

cd "$(dirname "$0")/.."

echo "=== Reproducing results for A Data-Driven Design Strategy for Next-Generation Lithium Batteries ==="
echo "Started at: $(date)"

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
if [ -f code/requirements.txt ]; then
    pip install -r code/requirements.txt
else
    echo "ERROR: code/requirements.txt not found!"
    exit 1
fi

# Step 2: Generate figures and run computations
echo "Step 2: Running experiment scripts..."

scripts=$(find code -name "*.py" -type f 2>/dev/null | sort)

if [ -z "$scripts" ]; then
    echo "ERROR: No Python scripts found in code/ directory!"
    exit 1
fi

count=0
for script in $scripts; do
    echo "Running $script ..."
    if python3 "$script"; then
        count=$((count+1))
        echo "✓ $script completed"
    else
        echo "✗ $script failed"
        exit 1
    fi
done

echo "Total scripts executed: $count"
echo "=== Done ==="
echo "Finished at: $(date)"
