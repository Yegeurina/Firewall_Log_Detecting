SELECT 
	FROM_UNIXTIME(log.korTime) AS KR_TIME, 
    FROM_UNIXTIME(log.usTime) AS US_TIME, 
    INET_NTOA(log.srcip) AS srcIP, 
    HEX(log.srcmac) AS serMAC,
    log.srcport AS srcPort,
    INET_NTOA(log.dstip) AS dstIP,
    HEX(log.dstmac) AS dstMAC,
    log.dstport AS dstPort,
    log.size AS PacketSize
FROM analysisfw.log log;