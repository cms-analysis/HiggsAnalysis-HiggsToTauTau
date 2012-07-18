#!/bin/bash

base=`pwd`
name="page.html"
#cd $base/${limit}/mssm
#harvest.py --prepAsym --strategy 1 cmb/* emu/* mutau/* etau/* incl/*
#cd ${limit}/sm
#harvest.py --prepAsym --strategy 1 cmb/* emu/* mutau/* etau/* boost/* vbf/* incl/*

cd $base

echo "<html>"                                                                >  $name
echo "<head><title>Htt Limit Plots</title></head>"                           >> $name
echo "<body bgcolor=\"FFFFFF\">"                                             >> $name
echo "<h3 style=\"text-align:left; color:DD6600;\"> Plots</h3>"              >> $name
echo "<table border=\"0\" cellspacing=\"5\" width=\"100%\">"                 >> $name

count=0
for x in `ls *.png | grep -v sample | grep -v prefit | grep -v datamc | grep -v 50`; do
    if [ $count -gt "1" ]; then echo "<tr>" >> $name ; fi
    if [ $count -gt "1" ]; then count=0 ; fi
    echo "<td width=\"50%\"><a href=\""${x}"\"><img src=\""${x}"\" alt=\""${x}"\" width=\"100%\"></a></td>" >> $name
    count=`echo "$count + 1" | bc`
done

echo "</table>"  >> $name
echo "<hr />"    >> $name
echo "</body>"   >> $name
echo "</html>"   >> $name

