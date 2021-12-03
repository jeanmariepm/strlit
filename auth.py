from os import write
from numpy import dtype
import streamlit as st
from db.stock_sql import StockSql

SS = StockSql()


def auth():
    # pick an action and run
    actions = [
        {'title': 'Login', 'function': login},
        {'title': 'Register', 'function': register},
    ]
    action = st.selectbox("Action",
                          actions,
                          format_func=lambda action: action['title']
                          )
    # run the action
    user = action['function']()
    return user


def login():
    username = st.text_input("Username:")
    if username:
        user = SS.fetchMember(username)
        if user:
            password = st.text_input("Enter Password:", type="password")
            if password:
                if password == user.password:
                    if user.is_su:
                        if st.checkbox("Check to edit user database"):
                            _superuser_mode()
                    else:
                        st.write('You are now logged in')
                    return user
                else:
                    st.error('Incorrect password')
                    return None
        else:
            st.error('Invalid username')
            return None


def register():
    username = st.text_input("Enter Username", value="")
    password = st.text_input("Enter Password (required)", value="")
    if st.button("Update Database") and username and password:
        user = SS.register(username, password)
        if user:
            st.text("Database Updated")
            return user
        st.error('Failed to register user')
        return None


def _list_users(users):
    st.write(users)


def _edit_users(users):
    usernames = ['<select>'] + users['username'].tolist()
    edit_user = st.selectbox("Select user", usernames)
    if edit_user != '<select>':
        st.write(f'TBD {edit_user} updated')


def _delete_users(users):
    usernames = ['<select>'] + users['username'].tolist()
    edit_user = st.selectbox("Select user", usernames)
    if edit_user != '<select>':
        st.write(f'TFD {edit_user} deleted')


def _superuser_mode():
    members = SS.listMembers()
    mode = st.radio("Select mode", ("View",  "Edit", "Delete"))
    {
        "View": _list_users,
        "Edit": _edit_users,
        "Delete": _delete_users,
    }[mode](members)


def run():
    return auth()


if __name__ == "__main__":
    st.write(
        "Warning, superuser mode\n\nUse this mode to initialise authentication database"
    )
    if st.checkbox("Check to continue"):
        _superuser_mode()
