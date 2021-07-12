---
title: Klaster
id: cluster
date: 2019-06-15
full_link: 
short_description: >
   Zestaw maszyn roboczych, nazywanych {{< glossary_tooltip text="węzłami" term_id="node" >}}, na których uruchamiane są aplikacje w kontenerach.
   Każdy klaster musi posiadać przynajmniej jeden węzeł.

aka: 
tags:
- fundamental
- operation
---
Zestaw maszyn roboczych, nazywanych węzłami, na których uruchamiane są aplikacje w kontenerach. Każdy klaster musi posiadać przynajmniej jeden węzeł.

<!--more-->
Na węźle (lub węzłach) roboczych rozmieszczane są {{< glossary_tooltip text="pody" term_id="pod" >}},
które są częściami składowymi aplikacji.
{{< glossary_tooltip text="Warstwa sterowania" term_id="control-plane" >}} zarządza
węzłami roboczymi i podami należącymi do klastra. W środowisku produkcyjnym warstwa sterowania
rozłożona jest zazwyczaj na kilka maszyn, a klaster uruchomiony jest na wielu węzłach zapewniając
większą niezawodność i odporność na awarie.
