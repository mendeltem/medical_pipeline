#! /bin/bash


alias mipavjava="/home/temuuleu/mipav/jre/bin/java -classpath /home/temuuleu/mipav/plugins/:/home/temuuleu/mipav/:`find /home/temuuleu/mipav/ -name \*.jar | sed 's#/home/temuuleu/mipav/#:/home/temuuleu/mipav/#' | tr -d '\n' | sed 's/^://'`"


#mipavjava edu.jhu.ece.iacl.jist.cli.runLayout /home/temuuleu/Belove_output/BLV-01-K-00059-M/new_layout.LayoutXML\
# -xClean -xDir /home/temuuleu/CSB_NeuroRad/temuuleu/Projekts/Belove/Belove_output/BLV-01-K-00059-M/


mipavjava edu.jhu.ece.iacl.jist.cli.runLayout $1\
 -xDir $2

#mipavjava edu.jhu.ece.iacl.jist.cli.runLayout $1\
# -xClean -xDir $2