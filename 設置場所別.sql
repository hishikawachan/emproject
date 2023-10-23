SELECT payplacecd,SUM(payprice) FROM tbpaylog
WHERE paydatedec >= 20230801
AND   paydatedec <= 20230831
AND   payplacecd IN(26,27)
GROUP BY payplacecd