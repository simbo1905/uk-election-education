#!/bin/bash
# Test runner that executes unit tests first, then integration tests
# Stops on first unit test failure, reports all integration test results

# Configuration
TESTS_DIR="./tests"
OUTPUT_DIR="./test_output"
UNIT_TEST_PATTERN="unit_test*.py"
INTEGRATION_TEST_PATTERN="integration_test_*.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize
echo -e "${BLUE}🚀 Starting Test Runner${NC}"
echo "=================================================="

# Clean and create output directory
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Function to run a single test
run_test() {
    local test_file="$1"
    local test_name
    test_name=$(basename "$test_file" .py)
    local output_file="$OUTPUT_DIR/${test_name}.log"
    
    echo -n "Running $test_name... "
    
    # Run test and capture output
    if python3 "$TESTS_DIR/run_one_test.py" "$test_file" > "$output_file" 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        echo "  See: $output_file"
        return 1
    fi
}

# Run unit tests first
echo -e "\n${YELLOW}📋 Running Unit Tests (Fast)${NC}"
echo "--------------------------------------------------"

unit_failed=0
unit_total=0

for test_file in $(find "$TESTS_DIR" -name "$UNIT_TEST_PATTERN" -type f | sort); do
    ((unit_total++))
    if ! run_test "$test_file"; then
        ((unit_failed++))
    fi
done

# Report unit test results
echo ""
if [ $unit_failed -eq 0 ]; then
    echo -e "${GREEN}🎉 All $unit_total unit tests passed!${NC}"
    echo ""
else
    echo -e "${RED}❌ $unit_failed of $unit_total unit tests failed${NC}"
    echo -e "${RED}Stopping here - fix unit tests before running integration tests${NC}"
    exit 1
fi

# Run integration tests
echo -e "${YELLOW}🔧 Running Integration Tests (Slow)${NC}"
echo "--------------------------------------------------"

integration_failed=0
integration_total=0

for test_file in $(find "$TESTS_DIR" -name "$INTEGRATION_TEST_PATTERN" -type f | sort); do
    ((integration_total++))
    if ! run_test "$test_file"; then
        ((integration_failed++))
    fi
done

# Final report
echo ""
echo "=================================================="
echo -e "${BLUE}📊 Test Summary${NC}"
echo "=================================================="
echo -e "Unit Tests:        ${GREEN}$((unit_total - unit_failed))/${unit_total} passed${NC}"
if [ $integration_total -gt 0 ]; then
    if [ $integration_failed -eq 0 ]; then
        echo -e "Integration Tests: ${GREEN}$((integration_total - integration_failed))/${integration_total} passed${NC}"
    else
        echo -e "Integration Tests: ${RED}$((integration_total - integration_failed))/${integration_total} passed${NC}"
    fi
fi

# Exit with appropriate code
if [ $integration_failed -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some integration tests failed${NC}"
    exit 1
fi
