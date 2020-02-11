# RikChan
A simple chan framework made in python

## Installation Guide
First run `setup.py` (it has no arguements). After that to make/manage accounts you have to use `account.py`.</br>
`python account.py <username> <password> <rank number>` </br>
This code generates a new account (Substitute values of username , password and rankid without the <>). Rankid represents authority. 
- 2 represents admin
- 1 represents moderator
- 0 represents janitor
</br>
If you want to change password of already existing account. Type</br>

`python account.py cp <username> <newpassword>`
Similarly for new rank id</br>

`python account.py cr <username> <newrank>`
If both needs to be changed</br>

`python account.py cpr <username> <newpassword> <newrank>`
</br>
If you want to create a new board. Go to `/_ct_` as admin.</br>
If you want to post as admin or moderator simply type `<username>#<password>#<the name you want to post as`. If you just want to post as your username type `<username>#<password>`




## Todo

- A system to login/logout for janitors/mods/admins
- A system to log the IP of poster (Chans are notorious, and I plan to delete the information of the poster once the post gets deleted)
- A system to show miscellaneous stuff along with the post
- Tripcode support