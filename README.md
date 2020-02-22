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
If you want to post as admin or moderator simply type `<username>#<password>#<the name you want to post as`. If you just want to post as your username type `<username>#<password>`</br>
RikChan already comes with 3 banners at `static/banners` folder. Put any image file in that folder (file shouldn't be hidden). And RikChan will load it up.</br>
</br>
To delete stuff as an admin, log in as admin and then mark with checkboxes just like how you will do in normal delete but you don't need to give any password.</br>

Suppose you want to ban ip address `123.456.789.012` just put it in the `ban.txt` file. Suppose you want to range ban `123.456.789.*` , then just put `123.456.789.` or `123.456.789` in `ban.txt`.</br>
If you are using a cloud based operator then for proper logging and banning you have to replace `request.remote_addr` with `request.headers['X-Real-IP']` (that is what most of the servers use. Ask your host if you have any problem, we have included commented code for the other use too, so you can uncomment and comment code line according to your need)

</br>
Working chan at <a href="https://rikchan.pythonanywhere.com">RikChan</a>


## Todo
- Archiving and pinning posts

## Credits
- The three banners that already come with RikChan are the work of an anonymous poster at <a href="https://rikchan.pythonanywhere.com">RikChan</a>