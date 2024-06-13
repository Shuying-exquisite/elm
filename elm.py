import streamlit as st
import subprocess
import os

def run_js_file(js_file_path, env_var):
    # 设置环境变量
    os.environ["elmck"] = env_var
    # 执行 JavaScript 文件
    subprocess.run(["node", js_file_path], check=True)

def main():
    st.title("执行 ele_elge.js 文件")

    # 在界面中添加输入框，以便用户输入 elmck 的值
    env_var = st.text_input("请输入 elmck 的值")

    if st.button("执行"):
        if env_var:
            # 当用户点击执行按钮时，调用函数执行 JavaScript 文件
            run_js_file("ele_elge.js", env_var)
        else:
            st.warning("请先输入 elmck 的值")

if __name__ == "__main__":
    main()
