#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

FIRST_DIR="${SCRIPT_DIR}/test_first_dir/"
SECOND_DIR="${SCRIPT_DIR}/test_second_dir/"
OUTPUT_DIR="${SCRIPT_DIR}/test_output_dir/"

EXEC="python ${SCRIPT_DIR}/diffcp.py"
OPT="--verbose --batch"

if [[ $1 == "clean" ]]; then
    echo "Cleaning output directory..."
    if [[ $( find ${OUTPUT_DIR} -type f ) ]]; then
        rm ${OUTPUT_DIR}* && \
            echo "Output directory successfully cleaned."
    else
        echo "Output directory already empty."
    fi
    exit 0
fi

echo "Testing diffcp.py..."
if [[ $( $EXEC $FIRST_DIR $SECOND_DIR $OUTPUT_DIR $OPT ) ]]; then
    echo "Test passed."
    exit 0
else
    echo "Test failed."
    exit 1
fi
