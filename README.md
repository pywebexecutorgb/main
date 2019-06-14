# Python web executer

"Веб-интерфейс с возможностью выполнения python-кода.
На выходе короткая ссылка с результатом выполнения, а также benchmark/профилирование.

Backend часть должна уметь:

- безопасно исполнять python-коде (rexec, chroot)
- выводить exception при некорректном синтаксисе
- сохранять код и результат его выполнения и, в дальнейшем, выдавать его без выполнения (sha-256 от кода)
- вывод результата профилирования (cProfile)

MVP+ (при условии, что хватит времени):

- чат с комментариями кода
- дизассемблирование строк кода (модуль dis)
- подсветка python синтаксиса (markdown)"

Перед началом работы нужно собрать стартовый образ docker с тегом web-executor-base  
из Dockerfile, который расположен в корневой директории проекта:

    $ docker build --tag web-executor-base --file Dockerfile .

