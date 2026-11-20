import streamlit as st


st.set_page_config(
    page_title="똑같이 나누고 합치는 분수·소수 실험실",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #f5f9ff; }
    h1, h2, h3 { color: #17365d; }
    [data-testid="stWidgetLabel"] { font-size: 1.1rem; font-weight: 650; }
    div.stButton > button {
        min-height: 3rem;
        border-radius: 0.8rem;
        font-size: 1.05rem;
        font-weight: 650;
    }
    .strip {
        display: flex;
        width: 100%;
        height: 3.8rem;
        overflow: hidden;
        border: 2px solid #315b7d;
        border-radius: 0.65rem;
        background: white;
        box-sizing: border-box;
    }
    .strip-part {
        flex: 1 1 0;
        min-width: 0;
        border-right: 2px solid #315b7d;
        box-sizing: border-box;
    }
    .strip-part:last-child { border-right: 0; }
    .strip-part.filled { background: #6bc7a5; }
    .strip-part.unfilled { background: #ffffff; }
    .strip-part.uneven-a { background: #d7e9f7; }
    .strip-part.uneven-b { background: #fce6b2; }
    .strip-caption {
        margin: 0.35rem 0 1rem;
        color: #425466;
        font-size: 1rem;
        text-align: center;
    }
    .decimal-value {
        margin: 0.65rem 0;
        color: #17365d;
        font-size: 1.7rem;
        font-weight: 750;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧪 똑같이 나누고 합치는 분수·소수 실험실")
st.markdown("막대를 직접 바꾸며 **분수와 소수의 크기와 뜻**을 알아봐요.")


def fraction_reading(numerator: int, denominator: int) -> str:
    number_names = (
        "영", "일", "이", "삼", "사", "오", "육",
        "칠", "팔", "구", "십", "십일", "십이",
    )
    return f"{number_names[denominator]}분의 {number_names[numerator]}"


def render_strip(denominator: int, numerator: int) -> None:
    parts = "".join(
        '<span class="strip-part filled"></span>'
        if part < numerator
        else '<span class="strip-part unfilled"></span>'
        for part in range(denominator)
    )
    st.markdown(
        f'<div class="strip" role="img" aria-label="{denominator}칸 중 '
        f'{numerator}칸 색칠">{parts}</div>',
        unsafe_allow_html=True,
    )


def render_uneven_strip() -> None:
    widths = (13, 27, 21, 39)
    parts = "".join(
        f'<span class="strip-part uneven-{"a" if index % 2 == 0 else "b"}" '
        f'style="flex: 0 0 {width}%"></span>'
        for index, width in enumerate(widths)
    )
    st.markdown(
        f'<div class="strip" role="img" aria-label="크기가 서로 다른 네 조각">'
        f'{parts}</div>',
        unsafe_allow_html=True,
    )


def render_decimal_strip(tenths: int) -> None:
    render_strip(10, tenths)
    st.markdown(
        f'<div class="decimal-value">{decimal_text(tenths)} '
        f'<span style="font-size:1.15rem;font-weight:500">'
        f'({tenths}/10)</span></div>',
        unsafe_allow_html=True,
    )


def decimal_text(tenths: int) -> str:
    return "1.0" if tenths == 10 else f"0.{tenths}"


fraction_tab, compare_tab, decimal_tab = st.tabs(
    ["🧩 똑같이 나누고 분수 만들기", "⚖️ 분수 크기 비교하기", "🔟 소수 알아보기"]
)

with fraction_tab:
    st.header("전체를 똑같이 나누어 볼까요?")
    st.write("막대 한 개가 전체예요. 똑같은 크기의 칸을 만들고 색칠해 보세요.")
    fraction_columns = st.columns(2)
    with fraction_columns[0]:
        denominator = st.slider(
            "몇 칸으로 똑같이 나눌까요?",
            min_value=2,
            max_value=12,
            value=4,
            key="fraction_denominator",
        )
    with fraction_columns[1]:
        numerator = st.slider(
            "몇 칸을 색칠할까요?",
            min_value=0,
            max_value=denominator,
            value=min(3, denominator),
            key="fraction_numerator",
        )

    render_strip(denominator, numerator)
    st.markdown(f"### 색칠한 부분은 **{numerator}/{denominator}**")
    st.markdown(f"읽는 법: **{fraction_reading(numerator, denominator)}**")
    st.caption("분모는 전체를 똑같이 나눈 칸 수, 분자는 색칠한 칸 수예요.")

    st.divider()
    st.subheader("비교해 보기: 똑같이 나누지 않으면?")
    st.write("아래 막대는 조각의 크기가 서로 달라요. 공평하게 나눈 분수로 나타낼 수 있을까요?")
    render_uneven_strip()
    st.warning("조각의 크기가 서로 다르면 ‘똑같이 나눈 것’이 아니므로, 분수로 나타낼 수 없어요.")

with compare_tab:
    st.header("두 분수 띠 중 어느 쪽이 더 길까요?")
    compare_mode = st.radio(
        "어떤 분수를 비교해 볼까요?",
        ["분자가 1인 분수", "분모가 같은 분수"],
        horizontal=True,
        key="fraction_compare_mode",
    )

    if compare_mode == "분자가 1인 분수":
        first_column, second_column = st.columns(2)
        with first_column:
            first_denominator = st.selectbox(
                "첫 번째 분모", options=range(2, 13), index=0, key="unit_first"
            )
        with second_column:
            second_denominator = st.selectbox(
                "두 번째 분모", options=range(2, 13), index=1, key="unit_second"
            )
        first_numerator = second_numerator = 1
    else:
        denominator = st.selectbox(
            "두 분수의 분모", options=range(2, 13), index=3, key="common_denominator"
        )
        first_column, second_column = st.columns(2)
        with first_column:
            first_numerator = st.select_slider(
                "첫 번째 분자",
                options=range(1, denominator + 1),
                value=min(2, denominator),
                key="common_first_numerator",
            )
        with second_column:
            second_numerator = st.select_slider(
                "두 번째 분자",
                options=range(1, denominator + 1),
                value=min(4, denominator),
                key="common_second_numerator",
            )
        first_denominator = second_denominator = denominator

    first_column, second_column = st.columns(2)
    with first_column:
        st.markdown(f"#### 첫 번째: {first_numerator}/{first_denominator}")
        render_strip(first_denominator, first_numerator)
    with second_column:
        st.markdown(f"#### 두 번째: {second_numerator}/{second_denominator}")
        render_strip(second_denominator, second_numerator)

    first_size = first_numerator * second_denominator
    second_size = second_numerator * first_denominator
    if first_size > second_size:
        st.success(f"**{first_numerator}/{first_denominator}** 쪽이 더 커요.")
    elif first_size < second_size:
        st.success(f"**{second_numerator}/{second_denominator}** 쪽이 더 커요.")
    else:
        st.info("두 분수의 크기가 같아요.")
    st.caption("두 띠는 같은 길이예요. 색칠된 부분의 길이를 눈으로 비교해 보세요.")

with decimal_tab:
    st.header("1을 열 칸으로 나누면 한 칸은 얼마일까요?")
    st.write("막대의 한 칸은 0.1이에요. 칸을 채우며 소수와 분수를 함께 살펴봐요.")
    tenths = st.slider(
        "몇 칸을 색칠할까요?",
        min_value=0,
        max_value=10,
        value=6,
        key="decimal_tenths",
    )
    render_decimal_strip(tenths)
    st.caption("소수 한 자리의 숫자는 0.1이 몇 개인지 알려줘요. 10/10은 1과 같아요.")

    st.divider()
    st.subheader("두 소수의 크기를 비교해 봐요")
    first_column, second_column = st.columns(2)
    with first_column:
        first_decimal = st.slider(
            "첫 번째 소수", min_value=0, max_value=10, value=4, key="first_decimal"
        )
        st.markdown(f"#### {decimal_text(first_decimal)}")
        render_strip(10, first_decimal)
    with second_column:
        second_decimal = st.slider(
            "두 번째 소수", min_value=0, max_value=10, value=8, key="second_decimal"
        )
        st.markdown(f"#### {decimal_text(second_decimal)}")
        render_strip(10, second_decimal)

    if first_decimal > second_decimal:
        st.success(f"{decimal_text(first_decimal)}이(가) 더 커요.")
    elif first_decimal < second_decimal:
        st.success(f"{decimal_text(second_decimal)}이(가) 더 커요.")
    else:
        st.info("두 소수의 크기가 같아요.")

    st.divider()
    st.subheader("미션: 0.4보다 크고 0.8보다 작은 소수 만들기")
    if "mission_active" not in st.session_state:
        st.session_state.mission_active = False
    if "mission_tenths" not in st.session_state:
        st.session_state.mission_tenths = 5
    if st.button("미션 시작하기", key="start_decimal_mission"):
        st.session_state.mission_active = True
        st.session_state.mission_tenths = 5
        st.session_state.mission_result = ""

    if st.session_state.mission_active:
        st.write("0.4와 0.8 사이에 들어가는 소수를 골라 보세요.")
        answer = st.slider(
            "내가 만든 소수",
            min_value=0,
            max_value=10,
            key="mission_tenths",
        )
        if st.button("내 답 확인하기", key="check_decimal_mission"):
            if 4 < answer < 8:
                st.session_state.mission_result = (
                    f"정답이에요! {decimal_text(answer)}은(는) 0.4보다 크고 0.8보다 작아요."
                )
            else:
                st.session_state.mission_result = (
                    "다시 생각해 봐요. 0.4와 0.8은 포함하지 않고 그 사이의 수를 골라요."
                )
        if st.session_state.get("mission_result"):
            st.info(st.session_state.mission_result)
