import streamlit as st
import json
import os

files = {
    "テクノロジ系": "technology_questions.json",
    "ストラテジ系": "strategy_questions.json",
    "マネジメント系": "management_questions.json"
}


# JSONファイルの読み込み関数
def load_quiz_data(file_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, file_name)
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"`{file_name}` ファイルが見つかりません。正しい場所に配置してください。")
        return {"questions": []}


# セッション情報の初期化
def initialize_session():
    if "page_id" not in st.session_state:
        st.session_state.page_id = "main"
        st.session_state.answers = []
        st.session_state.correct_count = 0


# ページを変更
def change_page(page_id):
    st.session_state.page_id = page_id


# ページ設定
def set_page_config():
    st.set_page_config(page_title="Original Quiz")
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


# 最初のページ
def main_page():
    st.markdown("<h1 style='text-align: center;'>🚀Original Quiz🚀</h1>", unsafe_allow_html=True)

    with st.form("start_form"):
        st.radio("カテゴリを選んでね", ["テクノロジ系", "ストラテジ系", "マネジメント系"], key="table_number")
        if st.form_submit_button("スタート！"):
            st.session_state.answers = []  # 初期化
            st.session_state.correct_count = 0
            change_page("page1")


# 問題ページ
def question_page(page_num, quiz_data):
    question_data = quiz_data["questions"][page_num]
    question = question_data["question"]
    options = question_data["options"]
    correct_answer = question_data["correct_answer"]

    remaining_questions = len(quiz_data["questions"]) - page_num - 1

    st.markdown(f"<h1 style='text-align: center;'>第{page_num + 1}問</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>あと {remaining_questions} 問</h3>", unsafe_allow_html=True)

    with st.form(f"form_{page_num}"):
        st.radio(question, options, key=f"answer_{page_num}")
        if st.form_submit_button("進む"):
            user_answer = st.session_state[f"answer_{page_num}"]
            if len(st.session_state.answers) <= page_num:
                st.session_state.answers.append({
                    "question": question,
                    "answer": user_answer,
                    "correct_answer": correct_answer
                })
            else:
                st.session_state.answers[page_num] = {
                    "question": question,
                    "answer": user_answer,
                    "correct_answer": correct_answer
                }

            if user_answer == correct_answer:
                st.session_state.correct_count += 1

            next_page = f"page{page_num + 2}" if page_num < len(quiz_data["questions"]) - 1 else "page_end"
            change_page(next_page)

    if page_num > 0:
        if st.button("戻る"):
            previous_page = f"page{page_num}" if page_num > 0 else "main"
            change_page(previous_page)

    if st.button("中断する"):
        initialize_session()
        change_page("main")


# 結果ページ
def results_page():
    st.markdown("<h1 style='text-align: center;'>あなたの回答結果</h1>", unsafe_allow_html=True)
    st.markdown("---")

    correct_count = st.session_state.correct_count
    total_questions = len(st.session_state.answers)

    st.markdown(f"<h3 style='text-align: center;'>正解数: {correct_count}/{total_questions}</h3>", unsafe_allow_html=True)

    for idx, ans in enumerate(st.session_state.answers, 1):
        question = ans["question"]
        user_answer = ans["answer"]
        correct_answer = ans["correct_answer"]
        result = "✅ 正解" if user_answer == correct_answer else "❌ 不正解"

        st.markdown(
            f"<div style='text-align: center;'>"
            f"第{idx}問: {question}<br>"
            f"あなたの回答: {user_answer} / 正解: {correct_answer} ({result})"
            f"</div>",
            unsafe_allow_html=True,
        )

    if st.button("最初のページに戻る"):
        initialize_session()
        change_page("main")


# メイン処理
def main():
    set_page_config()
    initialize_session()
    quiz_data = load_quiz_data()

    if st.session_state.page_id == "main":
        main_page()
    elif st.session_state.page_id == "page_end":
        results_page()
    else:
        page_num = int(st.session_state.page_id.replace("page", "")) - 1
        question_page(page_num, quiz_data)


if __name__ == "__main__":
    main()
