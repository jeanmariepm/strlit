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
    print('ayth returning:',  user)
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
                    st.write('You are now logged in')
                    return user
                else:
                    st.error('Incorrect password')
                    return None
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


def _list_users():
    table_data = conn.execute(
        "select username,password,su from users").fetchall()
    if table_data:
        table_data2 = list(zip(*table_data))
        st.table(
            {
                "Username": (table_data2)[0],
                "Password": table_data2[1],
                "Superuser?": table_data2[2],
            }
        )
    else:
        st.write("No entries in authentication database")


def _edit_users():
    userlist = [x[0]
                for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    edit_user = st.selectbox("Select user", options=userlist)
    if edit_user:
        user_data = conn.execute(
            "select username,password,su from users where username = ?", (
                edit_user,)
        ).fetchone()
        _create_users(
            conn=conn,
            init_user=user_data[0],
            init_pass=user_data[1],
            init_super=user_data[2],
        )


def _delete_users():
    userlist = [x[0]
                for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    del_user = st.selectbox("Select user", options=userlist)
    if del_user:
        if st.button(f"Press to remove {del_user}"):
            with conn:
                conn.execute(
                    "delete from users where username = ?", (del_user,))
                st.write(f"User {del_user} deleted")


def _superuser_mode():
    mode = st.radio("Select mode", ("View", "Create", "Edit", "Delete"))
    {
        "View": _list_users,
        "Create": _create_users,
        "Edit": _edit_users,
        "Delete": _delete_users,
    }[mode]()


def run():
    return auth()


if __name__ == "__main__":
    st.write(
        "Warning, superuser mode\n\nUse this mode to initialise authentication database"
    )
    if st.checkbox("Check to continue"):
        _superuser_mode()
