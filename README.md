# Tasks_PyTest_Selenium_Allure
 <b>В проекте присутствуют 2 шелл скрипта, решение задач по питону в разных варинатах.
 А также файл содержащий тесты для запуска с помощью pytest. </b>
 
  
 ####Стек: pytest + selenium + allure 
 
 ####Commands for terminal: 
 ###### Запускать из папки с проектом. Предварительно установить `selenium` и `allure` (`scoop` для `windows`, `brew` для `linux`)
 1. <b>Для запуска тестов и генерации отчета:</b> 
    
    pytest --alluredir=reports -s pytest_selenium_allure.py \
    allure serve reports  
    
    *(также можно использовать сочетание команд для allure `generate` и `open`)
 2. `shell` скрипты запускать с помощью команды `source` (`linux`)
 3. `python_tasks_from_skype_interview.py` запускать с помощью желаемого интерпретатора `python`