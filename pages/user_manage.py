import streamlit as st
from lib import get_db

def show_user_management():
    """显示用户管理页面"""
    st.title("用户管理")
    db = get_db()

    # 添加新用户
    add_new_user(db)

    # 用户列表
    st.subheader("用户列表")
    try:
        sql = "select user_name, is_running, user_group, task_group, browser_name, browser_count from users"
        users = db.execute(sql)
        st.dataframe(users)
        # if users:
        #     for user in users:
        #         col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 1, 1])
        #         with col1:
        #             st.write(user.get("user_name"))
        #         with col2:
        #             st.write(user["user_group"])
        #         # with col3:
        #         #     status = "活跃" if user["is_active"] else "禁用"
        #         #     st.write(status)
        #         # with col4:
        #         #     st.write(user["created_at"].strftime("%Y-%m-%d"))
        #         # with col5:
        #         #     if st.button("编辑", key=f"edit_{user['id']}"):
        #         #         st.session_state.editing_user = user
        # else:
        #     st.info("暂无用户")
    except Exception as e:
        st.error(f"获取用户列表失败: {e}")


def add_new_user(db):
    # 添加用户表单
    with st.expander("添加新用户"):
        with st.form("add_user_form"):
            new_username = st.text_input("用户名")
            new_email = st.text_input("邮箱")
            new_password = st.text_input("密码", type="password")
            is_active = st.checkbox("是否激活", value=True)
            submitted = st.form_submit_button("添加用户")

            if submitted:
                try:
                    # 在实际应用中应对密码进行哈希处理
                    user_id = db.insert("users", {
                        "username": new_username,
                        "email": new_email,
                        "password_hash": new_password,
                        "is_active": is_active
                    })
                    st.success(f"用户 {new_username} 已添加，ID: {user_id}")
                except Exception as e:
                    st.error(f"添加用户失败: {e}")