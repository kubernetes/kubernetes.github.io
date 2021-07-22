---
title: Kontener aplikacji
id: app-container
date: 2019-02-12
full_link:
short_description: >
  Kontener używany do uruchomenia części grupy zadań w podzie.

aka:
tags:
- workload
---
Kontenery aplikacji są podstawową grupą {{< glossary_tooltip text="kontenerów" term_id="container" >}} w {{< glossary_tooltip text="podzie" term_id="pod" >}}.

<!--more-->

W Kuberetesie {{< glossary_tooltip text="zadania" term_id="workload" >}} w podzie mogą mieć różny cykl życia i fazę w której są wykonywane.

Na przykład kontenery inicjalizujące mogą być wymagane do wstępnej konfiguracji i szybko kończą swoją pracę.

Następnie uruchamiane są kontenery aplikacji, których celem jest najczęściej ciągła praca, lub ich cykl życia jest znacznie dłuży niż cykl życia kontenerów inicjalizujących.

W najprostszej konfiguracji pod składa się tylko i wyłącznie z jednego kontenera - kontenera aplikacji.
