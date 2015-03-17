#!/bin/bash
set -x

mkdir -p nithin
mkdir -p ashok
mkdir -p archa
mkdir -p lowres

for fil in `ls`
do
	res=`jpeginfo -c $fil | awk '{print $2$3$4;}'`

	case "$res" in
		800x480)
			mv $fil lowres
			;;

		480x800)
			mv $fil lowres
			;;

		2848x2136)
			mv $fil ashok
			;;

		2136x2848)
			mv $fil ashok
			;;

		2304x3072)
			mv $fil archa
			;;

		3072x2304)
			mv $fil archa
			;;

		2112x2816)
			mv $fil archa
			;;

		2816x2112)
			mv $fil archa
			;;

		2448x3264)
			mv $fil archa
			;;

		3264x2448)
			mv $fil archa
			;;

		1600x1200)
			mv $fil nithin
			;;

		1200x1600)
			mv $fil nithin
			;;

		2592x1944)
			mv $fil nithin
			;;

		1944x2592)
			mv $fil nithin
			;;

		1232x1632)
			mv $fil nithin
			;;

		1632x1232)
			mv $fil nithin
			;;

		2048x1216)
			mv $fil nithin
			;;

		1216x2048)
			mv $fil nithin
			;;

		1944x2592)
			mv $fil nithin
			;;

		2592x1944)
			mv $fil nithin
			;;

		*)
			mkdir -p $res
			mv $fil $res
			;;
	esac
done

