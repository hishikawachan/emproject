SELECT *
FROM(
SELECT 'date','price','hour','count'
UNION
SELECT tbpaylog.paydatedec,tbpaylog.payprice,tbpaylog.payhour,count(tbpaylog.payprice)
FROM tbpaylog
WHERE payyear = 2023
AND paymonth = 9
AND payday >= 1
AND payday <= 10
AND payplacecd IN(1,2,3,24,25) 
GROUP BY tbpaylog.paydatedec, tbpaylog.payprice, tbpaylog.payhour
) AAA;

