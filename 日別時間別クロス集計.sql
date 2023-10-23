SELECT tbpaylog.paydatedec, 
	SUM(CASE WHEN tbpaylog.payhour = 0 THEN tbpaylog.payprice ELSE 0 END) AS "0時",
	SUM(CASE WHEN tbpaylog.payhour = 1 THEN tbpaylog.payprice ELSE 0 END) AS "1時",
	SUM(CASE WHEN tbpaylog.payhour = 2 THEN tbpaylog.payprice ELSE 0 END) AS "2時",
	SUM(CASE WHEN tbpaylog.payhour = 3 THEN tbpaylog.payprice ELSE 0 END) AS "3時",
	SUM(CASE WHEN tbpaylog.payhour = 4 THEN tbpaylog.payprice ELSE 0 END) AS "4時",
	SUM(CASE WHEN tbpaylog.payhour = 5 THEN tbpaylog.payprice ELSE 0 END) AS "5時",
	SUM(CASE WHEN tbpaylog.payhour = 6 THEN tbpaylog.payprice ELSE 0 END) AS "6時",
	SUM(CASE WHEN tbpaylog.payhour = 7 THEN tbpaylog.payprice ELSE 0 END) AS "7時",
	SUM(CASE WHEN tbpaylog.payhour = 8 THEN tbpaylog.payprice ELSE 0 END) AS "8時",
	SUM(CASE WHEN tbpaylog.payhour = 9 THEN tbpaylog.payprice ELSE 0 END) AS "9時",
	SUM(CASE WHEN tbpaylog.payhour = 10 THEN tbpaylog.payprice ELSE 0 END) AS "10時",
	SUM(CASE WHEN tbpaylog.payhour = 11 THEN tbpaylog.payprice ELSE 0 END) AS "11時",
	SUM(CASE WHEN tbpaylog.payhour = 12 THEN tbpaylog.payprice ELSE 0 END) AS "12時",
	SUM(CASE WHEN tbpaylog.payhour = 13 THEN tbpaylog.payprice ELSE 0 END) AS "13時",
	SUM(CASE WHEN tbpaylog.payhour = 14 THEN tbpaylog.payprice ELSE 0 END) AS "14時",
	SUM(CASE WHEN tbpaylog.payhour = 15 THEN tbpaylog.payprice ELSE 0 END) AS "15時",
	SUM(CASE WHEN tbpaylog.payhour = 16 THEN tbpaylog.payprice ELSE 0 END) AS "16時",
	SUM(CASE WHEN tbpaylog.payhour = 17 THEN tbpaylog.payprice ELSE 0 END) AS "17時",
	SUM(CASE WHEN tbpaylog.payhour = 18 THEN tbpaylog.payprice ELSE 0 END) AS "18時",
	SUM(CASE WHEN tbpaylog.payhour = 19 THEN tbpaylog.payprice ELSE 0 END) AS "19時",
	SUM(CASE WHEN tbpaylog.payhour = 20 THEN tbpaylog.payprice ELSE 0 END) AS "20時",
	SUM(CASE WHEN tbpaylog.payhour = 21 THEN tbpaylog.payprice ELSE 0 END) AS "21時",
	SUM(CASE WHEN tbpaylog.payhour = 22 THEN tbpaylog.payprice ELSE 0 END) AS "22時",
	SUM(CASE WHEN tbpaylog.payhour = 23 THEN tbpaylog.payprice ELSE 0 END) AS "23時"	
FROM tbpaylog
WHERE payyear = 2023
AND paymonth = 9
AND payday >= 1
AND payday <= 10
AND payplacecd IN(1,2,3,24,25) 
GROUP BY tbpaylog.paydatedec
ORDER BY tbpaylog.paydatedec ASC; 