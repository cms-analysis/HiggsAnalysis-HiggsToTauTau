if (("$#" != "1"))
then
  echo "Usage: setup_lowtb_dirs.sh [DIR]"
  exit
fi

DIRECTORY=$1

cp -r $DIRECTORY/300 $DIRECTORY/220
cp -r $DIRECTORY/300 $DIRECTORY/230
cp -r $DIRECTORY/300 $DIRECTORY/240
cp -r $DIRECTORY/300 $DIRECTORY/250

