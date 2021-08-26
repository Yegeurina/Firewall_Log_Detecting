SELECT 
	FROM_UNIXTIME(log.korTime) AS KR_TIME, 
    FROM_UNIXTIME(log.usTime) AS US_TIME, 
    INET_NTOA(log.srcip) AS srcIP,
    HEX(log.srcmac) AS srcMAC,
    log.srcport AS srcPort,
    INET_NTOA(log.dstip) AS dstIP,
    HEX(log.dstmac) AS dstMAC,
    log.dstport AS dstPort
FROM analysisfw.log log
WHERE
	/* 직원 중 업무시간 외에 접속 한 로그 */
	(
		EXISTS (
		 SELECT 1 
		 FROM 
			analysisfw.employee employee,
			analysisfw.srv srv
		 WHERE
			 (
				log.srcip = employee.ip AND log.srcmac = employee.mac AND log.dstip = srv.ip AND log.dstmac = srv.mac AND log.dstport = srv.srvPort
				AND 
				(
					(employee.`region` = "Korea" AND NOT (TIME(FROM_UNIXTIME(log.korTime)) >= "07:00:00" AND TIME(FROM_UNIXTIME(log.korTime)) <= "21:00:00" AND weekday(log.korTime)<5) )
					OR 
					(employee.`region` = "US" AND NOT (TIME(FROM_UNIXTIME(log.usTime)) >= "07:00:00" AND (TIME(FROM_UNIXTIME(log.usTime)) <= "21:00:00") AND weekday(log.usTime)<5))
				)
			)
			OR
			(
				log.dstip = employee.ip AND log.dstmac = employee.mac AND log.srcip = srv.ip AND log.srcmac = srv.mac AND log.srcport = srv.srvPort
				AND 
				(
					(employee.`region` = "Korea" AND NOT (TIME(FROM_UNIXTIME(log.korTime)) >= "07:00:00" AND TIME(FROM_UNIXTIME(log.korTime)) <= "21:00:00" AND weekday(TIME(FROM_UNIXTIME(log.korTime))<5) )
					OR 
					(employee.`region` = "US" AND NOT (TIME(FROM_UNIXTIME(log.usTime)) >= "07:00:00" AND (TIME(FROM_UNIXTIME(log.usTime)) <= "21:00:00") AND weekday(TIME(FROM_UNIXTIME(log.usTime))<5)))
				)
			)
			
		)
	)
	OR
		/* 직원에 포함되지 않는 로그 */
		(
			NOT EXISTS (
			 SELECT 1 
			 FROM 
				analysisfw.employee employee,
				anlaysisfw.srv srv
			 WHERE 
				 (
					(log.srcip = employee.ip AND log.srcmac = employee.mac AND log.dstip = srv.ip AND log.dstmac = srv.mac AND log.dstport = srv.srvPort)
				 OR
					(log.dstip = employee.ip AND log.dstmac = employee.mac AND log.srcip = srv.ip AND log.srcmac = srv.mac AND log.srcport = srv.srvPort)
				)
			)
		)
    );