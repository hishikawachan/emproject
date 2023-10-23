SELECT payplacecd,payprice,ps.placename,co.comname 
from tbpaylog  AS lg
INNER JOIN  tbplace AS ps
ON lg.payplacecd = ps.placecode
INNER JOIN  tbcompany AS co
ON ps.placecocode = co.comcode
WHERE paydatedec = 20231009