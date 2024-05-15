format:
	black test
	black applications

integration:
	./test/sat_scan_api/integration/run.sh