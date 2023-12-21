days=`ls -l | awk '{print $9}' | sort -n | tail -n1`

for i in $(seq 1 $days); do
	cd $i
	echo "===== Day $i ====="
	python3 sol.py < input.txt
	cd ..
done
	
