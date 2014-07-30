from collections import OrderedDict
#nontoxicproducts = OrderedDict()
#nontoxicproducts['2104']='Terra Nova<br />Poli Cr&#xe8;me'
#nontoxicproducts['2103']='Terra Nova<br />Nettyoeur &#xe0; Meubles'
#nontoxicproducts['2102']='Terra Nova<br />Pierre Ponce Liquide'
#nontoxicproducts['2101']='Terra Nova<br />Restaurateur &#xe0; M&#xe9;tal'
#nontoxicproducts['2100']='Terra Nova<br />NaturOil'
#nontoxicproducts['1823']='Circa 1850<br />B&#xe9;ton Nu'
#nontoxicproducts['1822']='Circa 1850<br />M&#xe9;tal Nu'
#nontoxicproducts['1821']='Circa 1850<br />Plancher Net'
#oilsproducts = OrderedDict()
#oilsproducts['1802']='Circa 1850<br />Huile d&#x27;abrasin'
#oilsproducts['1807']='Circa 1850<br />Huile Tung&#x27;n Teak'
#oilsproducts['2100']='Terra Nova<br />NaturOil'
#oilsproducts['760']='Circa 1850<br />Huile antique<br />danoise'
#oilsproducts['1817']='Circa 1850<br />Polyur&#xe9;thane &#xe0;<br />s&#xe9;chage rapide'
#oilsproducts['2707']='Circa 1850<br />Huile Tung&#x27;Teak<br />Qualit&#xe9; Marine'
#oilsproducts['2760']='Circa 1850<br />Huile antique<br />Qualit&#xe9; Marine'
#oilsproducts['2705']='Circa 1850<br />Vernis antique<br />en p&#xe2;te<br />Qualit&#xe9; Marine'
#oilsproducts['1815']='Circa 1850<br />Vernis ext&#xe9;rieur'
#oilsproducts['1418']='Circa 1850<br />Vernis Aqua'
#oilsproducts['1805']='Circa 1850<br />Vernis antique<br />en p&#xe2;te'
#oilsproducts['1809']='Circa 1850<br />Gel&#xe9;e de tourneurs'
#oilsproducts['1702']='Gaudreault Antiques<br />Huile d&#x27;abrasin'
#removersproducts = OrderedDict()
#removersproducts['1800']='Circa 1850<br />D&#xe9;capant &#xe0; meubles'
#removersproducts['1806']='Circa 1850<br />D&#xe9;capant en p&#xe2;te pour<br />peinture et vernis'
#removersproducts['1820']='Circa 1850<br />D&#xe9;capant  Doux'
#removersproducts['1801']='Circa 1850<br />Repolisseur &#xe0;<br />beaux meubles'
#removersproducts['1700']='Gaudreault Antiques<br />D&#xe9;capant pour Peinture<br />et Vernis &#xe0; la Brosse'
#removersproducts['1706']='Gaudreault Antiques<br />D&#xe9;capant pour Peinture et Vernis &#xe0; Formule &#xc8;paisse'
#removersproducts['1897']='Swing<br />D&#xe9;capants Professionels'
#primerproducts = OrderedDict()
#primerproducts['3100']='Prime-It'
#primerproducts['3133']='Prime-It Plus'
#primerproducts['3107']='Prep-Coat pour tapisserie'
#primerproducts['3150']='Wallpaper Hang-Rite pour tapisserie'
#primerproducts['1823']='Circa 1850<br />B&#xe9;ton Nu'
#primerproducts['1822']='Circa 1850<br />M&#xe9;tal Nu'
#specialproducts = OrderedDict()
#specialproducts['8100']='Klenk&#x27;s<br />&#xc9;mail &#xc9;poxy'
#specialproducts['7900']='Formule Suisse<br />&#xc9;mail &#xc9;poxy'
#specialproducts['8172']='Anti Yeux<br />de Poisson'
#specialproducts['1555']='Circa 1850<br />NU-LUSTRE-55'
#specialproducts['1527']='NU-LUSTRE-27<br />Formule &#xe0; pinceau'
#specialproducts['1557']='NU-LUSTRE-57<br />UV-R&#xc9;SISTANT'
#specialproducts['1566']='NU-LUSTRE-66<br />THERMOSTABLE'
#waxesproducts = OrderedDict()
#waxesproducts['1600']='Antiquax<br />Cires Sp&#xe9;ciaux'
#waxesproducts['3200']='Circa 1850<br />Super DeGooper'
#waxesproducts['1804']='Circa 1850<br />Nettoyeur &#xe0; Meubles'
#waxesproducts['1803']='Circa 1850<br />Huile de Citron'
#waxesproducts['2103']='Terra Nova<br />Nettyoeur &#xe0; Meubles'
#waxesproducts['2101']='Terra Nova<br />Restaurateur &#xe0; M&#xe9;tal'
#waxesproducts['2104']='Terra Nova<br />Poli Cr&#xe8;me'
#waxesproducts['1821']='Circa 1850<br />Plancher Net'
#stainproducts = OrderedDict()
#stainproducts['770']='Circa 1850<br />Stain&#x27;n Varnish'
#stainproducts['709']='Circa 1850<br />Teinture &#xe0; bois'
#stainproducts['705']='Circa 1850<br />Appr&#xea;t &#xe0; bois'
#stainproducts['400']='Circa 1850<br />Teinture Aqua'
#accessoriesproducts = OrderedDict()
#accessoriesproducts['1301']='Circa 1850<br />Gants de d&#xe9;capage'
#accessoriesproducts['1300']='Circa 1850<br />Grattoir en &#xe9;rable'
#accessoriesproducts['1302']='Circa 1850<br />Outil de d&#xe9;capage'
#accessoriesproducts['1303']='Circa 1850<br />Tampon de finition'
#accessoriesproducts['1310']='Circa 1850<br />Coton Fromage'
#accessoriesproducts['1315']='Circa 1850<br />Essentiels pour Teindre'
#accessoriesproducts['1316']='Circa 1850 Essentiels<br />pour Teindre et M&#xe9;langer'
#accessoriesproducts['1201']='Chair-Loc'

accessoriesproducts = OrderedDict()
accessoriesproducts['1301']='Circa 1850<br />Gants de d&#xe9;capage'
accessoriesproducts['1300']='Circa 1850<br />Grattoir en &#xe9;rable'
accessoriesproducts['1302']='Circa 1850<br />Outil de d&#xe9;capage'
accessoriesproducts['1303']='Circa 1850<br />Tampon de finition'
accessoriesproducts['1310']='Circa 1850<br />Coton Fromage'
accessoriesproducts['1315']='Circa 1850<br />Essentiels pour Teindre'
accessoriesproducts['1316']='Circa 1850 Essentiels<br />pour Teindre et M&#xe9;langer'
epoxiesproducts = OrderedDict()
epoxiesproducts['1201']='Chair-Loc'
epoxiesproducts['1518']=''
epoxiesproducts['1527']='NU-LUSTRE-27<br />Formule &#xe0; pinceau'
epoxiesproducts['1555']='Circa 1850<br />NU-LUSTRE-55'
epoxiesproducts['1557']='NU-LUSTRE-57<br />UV-R&#xc9;SISTANT'
epoxiesproducts['1566']='NU-LUSTRE-66<br />THERMOSTABLE'
glueremoversproducts = OrderedDict()
glueremoversproducts['3200']='Circa 1850<br />Super DeGooper'
glueremoversproducts['1824']=''
glueremoversproducts['3207']=''
glueremoversproducts['3230']=''
varnishremoversproducts = OrderedDict()
varnishremoversproducts['1800']='Circa 1850<br />D&#xe9;capant &#xe0; meubles'
varnishremoversproducts['1806']='Circa 1850<br />D&#xe9;capant en p&#xe2;te pour<br />peinture et vernis'
varnishremoversproducts['1820']='Circa 1850<br />D&#xe9;capant  Doux'
varnishremoversproducts['1801']='Circa 1850<br />Repolisseur &#xe0;<br />beaux meubles'
varnishremoversproducts['3200']='Circa 1850<br />Super DeGooper'
varnishremoversproducts['1700']='Gaudreault Antiques<br />D&#xe9;capant pour Peinture<br />et Vernis &#xe0; la Brosse'
varnishremoversproducts['1706']='Gaudreault Antiques<br />D&#xe9;capant pour Peinture et Vernis &#xe0; Formule &#xc8;paisse'
varnishremoversproducts['1897']='Swing<br />D&#xe9;capants Professionels'
varnishremoversproducts['3208']=''
oilsproducts = OrderedDict()
oilsproducts['1802']='Circa 1850<br />Huile d&#x27;abrasin'
oilsproducts['1807']='Circa 1850<br />Huile Tung&#x27;n Teak'
oilsproducts['1702']='Gaudreault<br />Tung Oil'
oilsproducts['2100']='Terra Nova<br />NaturOil'
oilsproducts['2142']=''
oilsproducts['760']='Circa 1850<br />Huile antique<br />danoise'
oilsproducts['2707']='Circa 1850<br />Huile Tung&#x27;Teak<br />Qualit&#xe9; Marine'
oilsproducts['2146']=''
oilsproducts['2147']=''
oilsproducts['2143']=''
polyproducts = OrderedDict()
polyproducts['2705']='Circa 1850<br />Vernis antique<br />en p&#xe2;te<br />Qualit&#xe9; Marine'
polyproducts['1815']='Circa 1850<br />Vernis ext&#xe9;rieur'
polyproducts['1817']='Circa 1850<br />Polyur&#xe9;thane &#xe0;<br />s&#xe9;chage rapide'
polyproducts['1418']='Circa 1850<br />Vernis Aqua'
polyproducts['1805']='Circa 1850<br />Vernis antique<br />en p&#xe2;te'
polyproducts['1809']='Circa 1850<br />Gel&#xe9;e de tourneurs'
primersproducts = OrderedDict()
primersproducts['3100']='Prime-It'
primersproducts['3133']='Prime-It Plus'
primersproducts['3107']='Prep-Coat pour tapisserie'
primersproducts['3150']='Wallpaper Hang-Rite pour tapisserie'
primersproducts['1823']='Circa 1850<br />B&#xe9;ton Nu'
primersproducts['1822']='Circa 1850<br />M&#xe9;tal Nu'
primersproducts['3211']=''
stainsproducts = OrderedDict()
stainsproducts['770']='Circa 1850<br />Stain&#x27;n Varnish'
stainsproducts['709']='Circa 1850<br />Teinture &#xe0; bois'
stainsproducts['400']='Circa 1850<br />Teinture Aqua'
stainsproducts['760']=''
stainsproducts['3220']=''
waxesproducts = OrderedDict()
waxesproducts['1600']='Antiquax<br />Cires Sp&#xe9;ciaux'
waxesproducts['1804']='Circa 1850<br />Super DeGooper'
waxesproducts['1803']='Circa 1850<br />Nettoyeur &#xe0; Meubles'
waxesproducts['2101']='Circa 1850<br />Huile de Citron'
waxesproducts['2102']='Terra Nova<br />Nettyoeur &#xe0; Meubles'
waxesproducts['2103']='Terra Nova<br />Restaurateur &#xe0; M&#xe9;tal'
waxesproducts['2104']='Terra Nova<br />Poli Cr&#xe8;me'
waxesproducts['1821']='Circa 1850<br />Plancher Net'
bathproducts = OrderedDict()
bathproducts['8100']='Klenk&#x27;s<br />&#xc9;mail &#xc9;poxy'
bathproducts['8170']=''
bathproducts['11101']=''
bathproducts['8172']='Anti Yeux<br />de Poisson'
bathproducts['8175']=''
bathproducts['8200']=''
bathproducts['7900']='Formule Suisse<br />&#xc9;mail &#xc9;poxy'
solventsproducts = OrderedDict()
solventsproducts['9000']=''
solventsproducts['9001']=''
solventsproducts['9008']=''
clearanceproducts = OrderedDict()

products = {
'accessories':accessoriesproducts,
'epoxies':epoxiesproducts,
'glueremovers':glueremoversproducts,
'varnishremovers':varnishremoversproducts,
'oils':oilsproducts,
'poly':polyproducts,
'primers':primersproducts,
'stains':stainsproducts,
'waxes':waxesproducts,
'bath':bathproducts,
'solvents':solventsproducts,
'clearance':clearanceproducts,
'':''
}
