import os
import csv
from models import *

CSV_FILE = "../users.csv"
columns = ["id", "name", "post", "post id"]

def Newid():
    try:
        with open(CSV_FILE, mode = "r",newline ='') as file:
            reader = csv.reader(file)
            max_id = max(int(row["id"]) for row in reader)
            return max_id+1
    except (FileNotFoundError, csv.Error):
        return 1

def saveUsuarioID (usuario: UserID):
    exist_users = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode = "a+",newline ='') as file:
        writer = csv.DictWriter(file, fieldnames = columns)
        if not exist_users:
            writer.writeheader()
        writer.writerow(usuario.model_dump())

def Createuser (usuario : UserBase):
    id = Newid()
    new_user  = saveUsuarioID(id=id,**usuario.model_dump())
    saveUsuarioID(new_user)
    return new_user

def show_user (id: int):
    with open(CSV_FILE) as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row["id"]) == id:
                return saveUsuarioID(**row)


def delete_user (id: int):
    user_deleted : Optional[UserBase]=None
    users = show_user()
    with open(CSV_FILE,mode = "w",newline ='') as file:
        writer = csv.DictWriter(file, fieldnames = columns)
        writer.writeheader()
        for user_ in users:
            if user_.id == id:
                user_deleted = user_
                continue
            writer.writerow(user_.model_dump())
    if user_deleted:
        dict_user_no_id = user_deleted.model_dump()
        del dict_user_no_id["id"]
        return UserBase(**dict_user_no_id)
