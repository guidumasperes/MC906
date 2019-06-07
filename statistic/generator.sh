#!/bin/bash
#!/home/andrietta/PycharmProjects/Ma_handson/venv/bin/python

for i in {1..1000}
do
      fst=$(stat -c %Y "data/coeficientscorrelation")
      echo $fst
      python3 main_statistics.py &
      while : ; do
        current=$(stat -c %Y "data/coeficientscorrelation")
        [[ $current -eq $fst ]] || break
      done
      kill -9 $!
done