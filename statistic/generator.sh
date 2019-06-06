#!/bin/bash
#!/home/andrietta/PycharmProjects/Ma_handson/venv/bin/python

for i in {1..21}
do
      fst=$(stat -c %Y "data/colisioncoordinates")
      echo $fst
      python3 main_statistics.py &
      while : ; do
        current=$(stat -c %Y "data/colisioncoordinates")
        [[ $current -eq $fst ]] || break
      done
      kill -9 $!
done