# $PERM="sudo"
# $COMMAND="python3"
# $PYFILE="Matrix.py"
FILENAME="file"


ARGS=(
  "1000 1000 50"
  "1000 1000 100"
  "2000 2000 50"
  "2000 2000 100"
  "3000 2000 50"
  "3000 2000 100"
  "4000 1000 50"
  "4000 1000 100"
  "5000 5000 50"
  "5000 5000 75"
  "5000 5000 100"
)

echo "Setting up tests...";

for (( i = 0; i < ${#ARGS[@]}; i++ )); do
  sudo python3 Matrix.py $FILENAME$i ${ARGS[i]}
done

echo "Done";
