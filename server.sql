SELECT 
    INET_NTOA(server.ip) AS IP, 
    HEX(server.mac) AS MAC,
    server.port AS Port
FROM analysisfw.server server;