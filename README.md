# basdatt

## Git dan Github 
(selengkapnya di: https://medium.com/devsaurus-class/tutorial-git-2020-d8c258b9e35f **dan**
https://www.atlassian.com/git/tutorials/syncing/git-push)
<pastiin udah punya akun github, terus janlup login github di vscode juga yeah>
## DOWNLOAD DAN INSTALASI ##
1) download dan install git (di windows): https://git-scm.com/download/win
2) config akun dengan membuka folder git di terminal **atau** buka GIT BASH, run command berikut
git config --global user.name "Nama siapa pun gerangan"
git config --global user.email "email_akun_github@example.com"

## macam-macam dengan repository ##
<command berikut di-run pada terminal folder yang sedang dikerjakan>




## Run di terminal ya!
- Di-run ketika men-generate file migrations dan membuat perubahan di models (nambahin fields, models, dll)
python manage.py makemigrations
python manage.py migrate

- Untuk run server, kemudian klik link: http://127.0.0.1:8000/
python manage.py runserver
