SCRIPTS=(
  "largestSquareBitwiseFast.py"
  # "largestSquareBitwise.py"
  "largestSquareNaiive.py"
  # "largestSquare.py"
)

TESTFILEBASE="file"
NUMTESTS=11

echo "Running tests..."
echo

for (( i = 0; i < NUMTESTS; i++ )); do
  echo "=============================================="
  echo "   [ Testing scripts against " $TESTFILEBASE$i "]"
  echo "=============================================="
  echo

  for j in ${SCRIPTS[@]}; do
    TESTFILE="$TESTFILEBASE$i"
    echo "====> " $j
    time python3 $j $TESTFILE
    echo
  done

done




echo
echo "Done"
