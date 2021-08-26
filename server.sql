SELECT 
    INET_NTOA(srv.ip) AS IP, 
    HEX(srv.mac) AS MAC,
    srv.srvPort AS srvPort
FROM analysisfw.srv srv;