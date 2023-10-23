SELECT tbplace.placename, sum(tbpaylog.payprice)
FROM tbpaylog
INNER JOIN tbplace
ON tbpaylog.payplacecd = tbplace.placecode
WHERE payyear = 2023
AND paymonth = 9
AND payday >= 1
AND payday <= 10
AND payplacecd IN(1,2,3,24,25)
group by tbplace.placename;
