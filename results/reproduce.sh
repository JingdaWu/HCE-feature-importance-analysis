#!/bin/bash
# Reproduce all results from the paper
# Run from the repository root: bash results/reproduce.sh
#
# Expected runtime: [document here]
# Random seeds: [document here if applicable]

set -e

cd "$(dirname "$0")/.."

echo "=== Reproducing results for A Data-Driven Design Strategy for Next-Generation \\Lithium Batteries: Feature-Guided Development of  \\Diluent for High-Performance Electrolytes ==="
echo "Started at: $(date)"

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
pip install -r code/requirements.txt

# Step 2: Generate figures and run computations
echo "Step 2: Running experiment scripts..."

scripts=$(find code -name "*.py" | sort)

count=0
for script in $scripts; do
    echo "Running $script ..."
    python3 "$script"
    count=$((count+1))
done

echo "Total scripts executed: $count"
echo "=== Done. Check figures or results for output. ==="
echo "Finished at: $(date)"
