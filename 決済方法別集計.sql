SELECT tbcard.cardname, sum(tbpaylog.payprice)
FROM tbpaylog
INNER JOIN tbcard
ON tbpaylog.paycardcd = tbcard.cardcode
WHERE payyear = 2023
AND paymonth = 9
AND payday >= 1
AND payday <= 10
AND payplacecd IN(1,2,3,24,25)
group by tbcard.cardname;