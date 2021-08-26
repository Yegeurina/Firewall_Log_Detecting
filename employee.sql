SELECT 
	employee.region AS Region,
    INET_NTOA(employee.ip) AS IP, 
    HEX(employee.mac) AS MAC
FROM analysisfw.employee employee;