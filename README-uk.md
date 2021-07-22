<!-- # The Kubernetes documentation -->
# Документація Kubernetes

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-main-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

<!-- This repository contains the assets required to build the [Kubernetes website and documentation](https://kubernetes.io/). We're glad that you want to contribute! -->
Вітаємо! В цьому репозиторії міститься все необхідне для роботи над [сайтом і документацією Kubernetes](https://kubernetes.io/). Ми щасливі, що ви хочете зробити свій внесок!

<!-- ## Running the website locally using Hugo -->
## Запуск сайту локально зa допомогою Hugo

<!-- See the [official Hugo documentation](https://gohugo.io/getting-started/installing/) for Hugo installation instructions. Make sure to install the Hugo extended version specified by the `HUGO_VERSION` environment variable in the [`netlify.toml`](netlify.toml#L10) file. -->
Для інструкцій з встановлення Hugo дивіться [офіційну документацію](https://gohugo.io/getting-started/installing/). Обов’язково встановіть розширену версію Hugo, яка позначена змінною оточення `HUGO_VERSION` у файлі [`netlify.toml`](netlify.toml#L10).

<!-- To run the website locally when you have Hugo installed: -->
Після встановлення Hugo, запустіть сайт локально командою:

```bash
git clone https://github.com/kubernetes/website.git
cd website
git submodule update --init --recursive --depth 1
make serve
```

<!-- This will start the local Hugo server on port 1313. Open up your browser to http://localhost:1313 to view the website. As you make changes to the source files, Hugo updates the website and forces a browser refresh. -->
Команда запустить локальний Hugo-сервер на порту 1313. Відкрийте у своєму браузері http://localhost:1313, щоб побачити сайт. По мірі того, як ви змінюєте вихідний код, Hugo актуалізує сайт відповідно до внесених змін і оновлює сторінку у браузері.

<!-- ## Get involved with SIG Docs -->
## Спільнота, обговорення, внесок і підтримка

<!-- Learn more about SIG Docs Kubernetes community and meetings on the [community page](https://github.com/kubernetes/community/tree/master/sig-docs#meetings). -->
Дізнайтеся, як долучитися до спільноти Kubernetes на [сторінці спільноти](http://kubernetes.io/community/).

<!-- You can also reach the maintainers of this project at: -->
Для зв’язку із супроводжуючими проекту скористайтеся:

- [Slack](https://kubernetes.slack.com/messages/sig-docs)
- [Поштова розсилка](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

<!-- ## Contributing to the docs -->
## Внесок у документацію

<!-- You can click the **Fork** button in the upper-right area of the screen to create a copy of this repository in your GitHub account. This copy is called a *fork*. Make any changes you want in your fork, and when you are ready to send those changes to us, go to your fork and create a new pull request to let us know about it. -->
Ви можете створити копію цього репозиторія у своєму акаунті на GitHub, натиснувши на кнопку **Fork**, що розташована справа зверху. Ця копія називатиметься *fork* (відгалуження). Зробіть будь-які необхідні зміни у своєму відгалуженні. Коли ви будете готові надіслати їх нам, перейдіть до свого відгалуження і створіть новий pull request, щоб сповістити нас.

<!-- Once your pull request is created, a Kubernetes reviewer will take responsibility for providing clear, actionable feedback.  As the owner of the pull request, **it is your responsibility to modify your pull request to address the feedback that has been provided to you by the Kubernetes reviewer.** -->
Після того, як ви створили pull request, рецензент Kubernetes зобов’язується надати вам по ньому чіткий і конструктивний коментар. **Ваш обов’язок як творця pull request - відкоригувати його відповідно до зауважень рецензента Kubernetes.**

<!-- Also, note that you may end up having more than one Kubernetes reviewer provide you feedback or you may end up getting feedback from a Kubernetes reviewer that is different than the one initially assigned to provide you feedback. -->
Також, зауважте: може статися так, що ви отримаєте коментарі від декількох рецензентів Kubernetes або від іншого рецензента, ніж той, якого вам було призначено від початку.

<!-- Furthermore, in some cases, one of your reviewers might ask for a technical review from a Kubernetes tech reviewer when needed.  Reviewers will do their best to provide feedback in a timely fashion but response time can vary based on circumstances. -->
Крім того, за потреби один із ваших рецензентів може запросити технічну перевірку від одного з технічних рецензентів Kubernetes, коли це необхідно. Рецензенти намагатимуться відреагувати вчасно, проте час відповіді може відрізнятися в залежності від обставин.

<!-- For more information about contributing to the Kubernetes documentation, see: -->
Більше інформації про внесок у документацію Kubernetes ви знайдете у наступних джерелах:

* [Внесок: з чого почати](https://kubernetes.io/docs/contribute/)
* [Використання шаблонів сторінок](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Керівництво зі стилю оформлення документації](http://kubernetes.io/docs/contribute/style/style-guide/)
* [Переклад документації Kubernetes іншими мовами](https://kubernetes.io/docs/contribute/localization/)

<!-- ## Localization `README.md`'s -->
## Файл `README.md` іншими мовами

| інші мови  | інші мови |
|-------------------------------|-------------------------------|
| [Англійська](README.md)       | [Французька](README-fr.md)    |
| [Корейська](README-ko.md)     | [Німецька](README-de.md)      |
| [Португальська](README-pt.md) | [Хінді](README-hi.md)         |
| [Іспанська](README-es.md)     | [Індонезійська](README-id.md) |
| [Китайська](README-zh.md)     | [Японська](README-ja.md)      |
| [В'єтнамська](README-vi.md)   | [Російська](README-ru.md)     |
| [Італійська](README-it.md)    | [Польська](README-pl.md)      |

<!-- ## Code of conduct -->
## Кодекс поведінки

<!-- Participation in the Kubernetes community is governed by the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md). -->
Участь у спільноті Kubernetes визначається правилами [Кодексу поведінки СNCF](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).

<!-- ## Thank you! -->
## Дякуємо!

<!-- Kubernetes thrives on community participation, and we appreciate your contributions to our website and our documentation! -->
Долучення до спільноти - запорука успішного розвитку Kubernetes. Ми цінуємо ваш внесок у наш сайт і документацію!
