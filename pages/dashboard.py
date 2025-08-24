import streamlit as st
from lib import get_db

def show_dashboard():
    """显示仪表板页面"""
    st.title("仪表板")

    # 显示用户信息
    if st.session_state.user_info:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("管理员信息")
            st.write(f"用户名: {st.session_state.user_info['username']}")
            st.write(f"注册时间: {st.session_state.user_info['created_at']}")

        with col2:
            st.subheader("系统状态")

            # 获取系统统计信息
            try:
                db = get_db()

                user_count = db.count("users")
                active_users = db.count("users", 'is_running = 1')

                st.metric("总用户数", user_count)
                st.metric("活跃用户", active_users)
                st.metric("今日访问", "243")
            except Exception as e:
                st.error(f"获取统计信息失败: {e}")

    # 其他仪表板内容...
    st.subheader("最近活动")
    # 这里可以显示最近的活动记录