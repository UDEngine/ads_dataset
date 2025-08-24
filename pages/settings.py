import streamlit as st

from lib import get_db


def show_settings():
    """显示系统设置页面"""
    st.title("系统设置")
    db = get_db()
    # 系统配置表单
    with st.form("system_settings"):
        st.subheader("基本设置")
        site_name = st.text_input("网站名称", "我的管理系统")
        site_description = st.text_area("网站描述", "这是一个功能强大的管理系统")
        enable_notifications = st.checkbox("启用通知", value=True)

        submitted = st.form_submit_button("保存设置")
        if submitted:
            st.success("设置已保存")

    # 个人资料设置
    st.subheader("个人资料")
    with st.form("profile_form"):
        current_email = st.session_state.user_info.get('email', '')
        new_email = st.text_input("邮箱", current_email)
        new_password = st.text_input("新密码", type="password")
        confirm_password = st.text_input("确认密码", type="password")

        submitted = st.form_submit_button("更新资料")
        if submitted:
            if new_password and new_password != confirm_password:
                st.error("密码不一致")
            else:
                try:
                    # 更新用户信息
                    update_data = {"email": new_email}
                    if new_password:
                        update_data["password_hash"] = new_password

                    db.update(
                        "users",
                        update_data,
                        "id = %s",
                        (st.session_state.user_info["id"],)
                    )
                    st.success("资料已更新")
                except Exception as e:
                    st.error(f"更新资料失败: {e}")