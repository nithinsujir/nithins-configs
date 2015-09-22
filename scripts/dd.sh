#!/bin/bash
#set -x

THREADS=${1:-1}
LOOPS=${2:-9999}
DEVICE=${3:-umema}
echo "Threads: $1"

memthrottle -r $$

for ((i = 0; i < 9999; i++)); do
	echo
	echo
	echo "================== Iteration $i ===================="

	start=$SECONDS
	echo
	echo "----------------- default write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 1k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=1k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 4k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=4k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 8k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=8k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 16k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=16k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 32k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=32k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 64k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=64k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 128k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=128k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 256k write size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/zero of=/dev/$DEVICE bs=256k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"


	start=$SECONDS
	echo
	echo "----------------- default read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 1k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=1k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 4k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=4k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 8k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=8k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo "----------------- 16k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=16k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"


	start=$SECONDS
	echo
	echo
	echo "----------------- 32k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=32k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 64k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=64k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 128k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=128k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	start=$SECONDS
	echo
	echo
	echo "----------------- 256k read size -----------------------------------------"
	for (( i = 0; i < $THREADS; i++ )); do
		dd if=/dev/$DEVICE of=/dev/null bs=256k &
	done
	wait
	dur=$(($SECONDS - $start))
	throughput=$(($THREADS * 1024 / $dur))
	echo "$throughput MB/s"

	sleep 5
done

