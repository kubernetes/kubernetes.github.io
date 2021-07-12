---
title: Kops
id: kops
date: 2018-04-12
full_link: /docs/getting-started-guides/kops/
short_description: >
Herramienta de línea de comandos que facilita la creación, destrucción, actualización y mantenimiento de clústeres de Kubernetes en alta disponibilidad para entornos de producción. *NOTA: Oficialmente solo soporta AWS, aunque también ofrece soporte para GCE en beta y WMware vSphere en versión alpha*.

aka:
tags:
- tool
- operation
---
 Herramienta de línea de comandos que facilita la creación, destrucción, actualización y mantenimiento de clústeres de Kubernetes en alta disponibilidad para entornos de producción. *NOTA: Oficialmente solo soporta AWS, aunque también ofrece soporte para GCE en beta y WMware vSphere en versión alpha*.

<!--more-->

`kops` provisiona el clúster con:

  * Instalación totalmente automatizada
  * Identificación de clúster basada en DNS
  * Autoreparación ya que todo se ejecuta en grupos de instancias gestionados
  * Soporte de Sistema Operativo limitado (Debian como opción recomendada, aunque soporta versiones de Ubuntu posteriores a la 16.04 y también ofrece soporte experimental para CentOS y RHEL)
  * Soporte de Alta disponibilidad (HA)
  * Habilidad para provisionar directamente la plataforma o generar los _manifests_ de Terraform equivalentes como salida

También puedes construir tu propio clúster utilizando directamente {{< glossary_tooltip term_id="kubeadm" >}}, que es la herramienta en la que se basa `kops`.
