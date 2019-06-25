{% with remote=remote_directory|default:"" %}
{% with requirements=requirements_path|default:"requirements.txt" %}
{% with script=script_filename|default:"exec.py" %}
{% with interpreter=python_interpreter|default:"python3" %}

FROM web-executor-base
MAINTAINER Andrey Kiselev "kiselevandrew@yandex.ru"

USER exec-user
WORKDIR /home/exec-user

COPY {{script}} {{remote}}/{{script}}

{% if use_pip %}
    COPY {{requirements}} {{remote}}/{{requirements}}
    RUN pip{% if interpreter == 'python3' %}3{% endif %} install --user -r {{remote}}/{{requirements}}
{% endif %}

CMD ["{{interpreter}}", "-u", "-m", "cProfile", "-s", "time", "{{remote}}/{{script}}"]

{% endwith %}
{% endwith %}
{% endwith %}
{% endwith %}