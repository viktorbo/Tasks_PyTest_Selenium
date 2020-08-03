# Tasks_PyTest_Selenium_Allure
 <b>В проекте присутствуют 2 шелл скрипта, решение задач по питону в разных варинатах.
 А также файл содержащий тесты для запуска с помощью pytest. </b>
 
  
 ####Стек: pytest + selenium + allure 
 
 ####Commands for terminal: 
 ###### Запускать из папки с проектом. Предварительно установить `python`, `selenium` и `allure` (`scoop` для `windows`, `brew` для `linux`)
 <b>Для запуска тестов и генерации отчета:</b> 
    
       
    pytest --alluredir=reports -s -v pytest_selenium_allure.py \
    allure serve reports  
    
    *(также можно использовать сочетание команд для allure `generate` и `open`)

 -  *(только для `linux`) \
    для запуска тестов и автоматической сборки репортинга запустить скрипт `linux_run_test.sh`  
 
 - `shell` скрипты запускать с помощью команды `source` (`linux`)
 
 - `python_tasks_from_skype_interview.py` запускать с помощью желаемого интерпретатора `python`
 
* Будьте внимательны! Проект подразумевает наличие вебдрайвера для работы selenium
