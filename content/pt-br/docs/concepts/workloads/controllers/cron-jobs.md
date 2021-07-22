---
reviewers:
- erictune
- soltysh
- janetkuo
title: CronJob
content_type: concept
weight: 80
---

<!-- visão geral -->

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

Um _CronJob_ cria {{< glossary_tooltip term_id="job" text="Jobs" >}} em um cronograma recorrente.

Um objeto CronJob é como uma linha em um arquivo _crontab_ (tabela cron). Executa uma tarefa periodicamente em um determinado cronograma, escrito no formato [Cron](https://en.wikipedia.org/wiki/Cron).

{{< caution >}}

Todos os horários da propriedade `schedule:` do  *CronJob* são baseadas no fuso horário do {{< glossary_tooltip term_id="kube-controller-manager" >}}.

Se a camada de gerenciamento do cluster executa o kube-controller-manager em Pods ou contêineres avulsos, o fuso horário configurado para o contêiner executando o kube-controller-manager determina o fuso horário que o controlador dos objetos CronJob utiliza.

{{< /caution >}}

Ao criar o manifesto para um objeto CronJob, verifique se o nome que você forneceu é um [nome de subdomínio DNS](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names) válido.
O nome não pode ter mais que 52 caracteres. Esta limitação existe porque o controlador do CronJob adicionará automaticamente 11 caracteres ao final do nome de tarefa escolhido, e o comprimento máximo de um nome de tarefa não pode ultrapassar 63 caracteres.

<!-- body -->

## CronJob

CronJobs são úteis para criar tarefas periódicas e recorrentes, como a execução de _backups_ ou o envio de mensagens de e-mail. CronJobs também permitem o agendamento de tarefas individuais para um horário específico, como por exemplo uma tarefa que executa quando a chance do cluster estar ocioso é maior.

### Exemplo

Este manifesto de CronJob de exemplo imprime o horário atual e uma mensagem dizendo olá a cada minuto:

{{< codenew file="application/job/cronjob.yaml" >}}

(O artigo [Running Automated Tasks with a CronJob](/docs/tasks/job/automated-tasks-with-cron-jobs/) demonstra este exemplo com maiores detalhes).

### Sintaxe do cronograma cron

```
# ┌───────────── minuto (0 - 59)
# │ ┌───────────── hora (0 - 23)
# │ │ ┌───────────── dia do mês (1 - 31)
# │ │ │ ┌───────────── mês (1 - 12)
# │ │ │ │ ┌───────────── dia da semana (0 - 6) (domingo a sábado;
# │ │ │ │ │                                 7 também representa domingo em alguns sistemas operacionais)
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
```

| Expressão 								| Descrição																								  	| Equivalente a |
| ------------- 						| ------------- 																							|-------------  |
| @yearly (ou @annually)		| Executa uma vez por ano, à meia-noite de 1º de janeiro 			| 0 0 1 1 * 		|
| @monthly 									| Executa uma vez por mês, à meia-noite do primeiro dia do mês| 0 0 1 * * 		|
| @weekly 									| Executa uma vez por semana, à meia-noite de domingo					| 0 0 * * 0 		|
| @daily (ou @midnight)			| Executa uma vez por dia, à meia-noite												| 0 0 * * * 		|
| @hourly 									| Executa uma vez por hora, no minuto zero         			  		| 0 * * * * 		|

Por exemplo, a linha abaixo determina que a tarefa deve iniciar toda sexta-feira à meia-noite, bem como em todo dia 13 do mês à meia-noite:

`0 0 13 * 5`

É também possível gerar expressões de cronograma para CronJobs utilizando ferramentas da _web_ como o [crontab.guru](https://crontab.guru/).

## Limitações do CronJob

Um CronJob cria uma tarefa _aproximadamente_ uma vez por tempo de execução de seu cronograma. Dizemos "aproximadamente" porque existem circunstâncias em que duas tarefas podem ser criadas, e outras circunstâncias em que nenhuma tarefa será criada. Tentamos tornar estas situações raras, mas não preveni-las completamente. Portanto, as tarefas devem ser _idempotentes_.

Se o valor da propriedade `startingDeadlineSeconds` (limite de tempo de inicialização, em segundos) estiver definido como um valor grande, ou não definido (o padrão), e se a propriedade `concurrencyPolicy` (política de concorrência) estiver definido como `Allow` (permitir), as tarefas sempre serão executadas pelo menos uma vez.

{{< caution >}}

Se a propriedade `startingDeadlineSeconds` estiver definida com um valor menor que 10 segundos, a tarefa cron poderá não ser agendada. Isso ocorre porque o cronograma de execução do {{< glossary_tooltip term_id="controller" text="controlador" >}} do CronJob verifica tarefas a cada 10 segundos.

{{< /caution >}}

Para cada CronJob, o {{< glossary_tooltip term_id="controller" text="controlador" >}} do CronJob verifica quantos agendamentos foram perdidos no tempo entre o último horário agendado e o horário atual. Se houver mais de 100 agendamentos perdidos no período, o controlador não iniciará o trabalho e gerará a seguinte mensagem de erro:

```
Cannot determine if job needs to be started. Too many missed start time (> 100). Set or decrease .spec.startingDeadlineSeconds or check clock skew.
```

É importante observar que, se o campo `startingDeadlineSeconds` estiver definido (não `nil`), o controlador contará quantas tarefas perdidas ocorreram a partir do valor de `startingDeadlineSeconds` até agora, e não do último horário agendado até agora. Por exemplo, se `startingDeadlineSeconds` for `200`, o controlador contará quantas tarefas perdidas ocorreram nos últimos 200 segundos.

Um CronJob é considerado perdido se não for criado no horário agendado. Por exemplo, se `concurrencyPolicy` estiver definido como `Forbid` (proibir) e uma tentativa de agendamento de um novo CronJob ocorreu quando havia um agendamento anterior ainda em execução, o novo agendamento será contabilizado como perdido.

Por exemplo, suponha que um CronJob esteja definido para agendar uma nova tarefa a cada minuto, começando às `08:30:00`, e seu campo `startingDeadlineSeconds` não esteja definido. Se o controlador do CronJob estiver inativo das `08:29:00` até as `10:21:00`, a tarefa não será iniciada, pois o número de tarefas que perderam seus horários agendados é maior que 100.

Para ilustrar melhor este conceito, suponha que um CronJob esteja definido para agendar uma nova tarefa a cada minuto, começando às `08:30:00`, e seu `startingDeadlineSeconds` esteja definido em 200 segundos. Se o controlador do CronJob estiver inativo no mesmo período do exemplo anterior (das `08:29:00` às `10:21:00`), a tarefa ainda será iniciada às 10:22:00. Isso acontece pois o controlador agora verifica quantos agendamentos perdidos ocorreram nos últimos 200 segundos (ou seja, 3 agendamentos perdidos), ao invés de verificar o período entre o último horário agendado e o horário atual.

O CronJob é responsável apenas pela criação das tarefas que correspondem à sua programação, e a tarefa, por sua vez, é responsável pelo gerenciamento dos Pods que ele representa.

## Versão do controlador

A partir da versão 1.21 do Kubernetes, a segunda versão do controlador do CronJob é a implementação ativada por padrão. Para desativar o controlador do CronJob padrão e utilizar a versão original do controlador do CronJob, é necessário adicionar o _flag_ de [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) `CronJobControllerV2` à chamada do {{< glossary_tooltip term_id="kube-controller-manager" >}} com o valor `false` (falso). Por exemplo:
```
--feature-gates="CronJobControllerV2=false"
```


## {{% heading "whatsnext" %}}

A página [Cron expression format](https://en.wikipedia.org/wiki/Cron) documenta o formato dos campos de agendamento do CronJob.

Para instruções sobre criação e utilização de tarefas cron, e para um exemplo de manifesto de CronJob, veja
[Running automated tasks with cron jobs](/docs/tasks/job/automated-tasks-with-cron-jobs).
