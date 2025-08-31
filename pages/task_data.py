from datetime import date, timedelta
import streamlit as st
from lib import get_db
from pages.user_manage import get_user_info


def show_task_data():

    """显示任务管理页面"""
    st.title("任务管理")
    db = get_db()

    # 取出任务数据
    tasks = get_task_info(db)

    # 取出用户数据
    users = get_user_info(db)

    # 创建两列布局
    col1, col2, col3 = st.columns(3)

    with col1:
        # 创建一个日期范围选择器
        st.subheader("选择任务ID")

        task_id_list = [task['task_id'] for task in tasks]
        task_id_list.insert(0, "All_Task")

        # 创建一个任务ID下拉选择框
        selected_task = st.selectbox(
            label="选择任务ID",  # 选择框的标签
            options=task_id_list,  # 下拉选项列表
            index=0,  # 默认选中第一个选项
            help="请选择一个任务ID"  # 帮助文本
        )

    with col2:
        # 用户选择
        st.subheader("选择用户")

        user_list = [user['user_name'] for user in users]
        user_list.insert(0, "All_User")

        # 创建一个任务ID下拉选择框
        selected_task = st.selectbox(
            label="选择用户",  # 选择框的标签
            options=task_id_list,  # 下拉选项列表
            index=0,  # 默认选中第一个选项
            help="请选择一个用户"  # 帮助文本
        )

    with col3:
        # 创建一个日期范围选择器
        st.subheader("选择日期范围")

        # 创建两列布局
        date_col1, date_col2 = st.columns(2)

        with date_col1:
            # 使用两个日期选择器来实现日期范围选择
            start_date = st.date_input(
                label="开始日期",
                value=date.today() - timedelta(days=7),  # 默认值为7天前
                min_value=date(2020, 1, 1),
                max_value=date.today(),
                help="请选择开始日期"
            )

        with date_col2:
            end_date = st.date_input(
                label="结束日期",
                value=date.today(),  # 默认值为今天
                min_value=date(2020, 1, 1),
                max_value=date.today() + timedelta(days=365),
                help="请选择结束日期"
            )

    # 可以根据选择执行一些操作
    if st.button("查询数据", type="primary"):
        # 这里可以添加查询数据库的代码
        with st.spinner("正在查询数据..."):
            st.write(start_date)
            st.write(end_date)
            st.write(selected_task)
            # 模拟数据库查询
            st.success("查询完成!")




    # 任务列表
    st.subheader("任务列表")
    st.dataframe(tasks, height=800)
    # # 可以根据选择执行一些操作
    # if st.button("任务列表", type="primary"):
    #     # 这里可以添加查询数据库的代码
    #     with st.spinner("正在查询数据..."):
    #         st.dataframe(tasks, height=800)
    #         st.success("查询完成!")


def get_task_info(db):
    try:
        sql = "select task_id, is_run, task_name, channel, task_group, weight, click_rate, tasks.task_urls, updated_at from tasks"
        return db.execute(sql)
    except Exception as e:
        st.error(f"获取任务列表失败: {e}")