import streamlit as st
from pathlib import Path
import base64
from typing import Optional


DRIVE_FOLDERS = {
    "LLAVES": "1ejw6eo2jpGb1F47MzLOY7vmkEQX0ZErQ",
    "ZONAS": "1RLjNhvMBTYfhNuHw-5vM4bY3494wSLsq",
}

LOGO_CANDIDATES = [
    Path("assets/logomodena.jpg"),
    Path("assets/modena_logo.jpg"),
    Path("assets/logomodena.jpeg"),
    Path("assets/logomodena.png"),
]


def get_logo_path() -> Optional[Path]:
    return next((path for path in LOGO_CANDIDATES if path.exists()), None)


def folder_embed_url(folder_id: str) -> str:
    return f"https://drive.google.com/embeddedfolderview?id={folder_id}#grid"


def folder_share_url(folder_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{folder_id}"


def render_folder(name: str, folder_id: str) -> None:
    st.subheader(name)
    st.markdown(f"[Open in Google Drive]({folder_share_url(folder_id)})")
    st.components.v1.iframe(folder_embed_url(folder_id), height=900, scrolling=True)


def set_logo_background() -> None:
    logo_path = get_logo_path()
    if logo_path is not None:
        logo_base64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-image:
                        linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
                        url('data:image/jpeg;base64,{logo_base64}');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Add the logo file in assets/ (for example: logomodena.jpg) to display the venue image.")


def set_text_colors() -> None:
    st.markdown(
        """
        <style>
            h1, h2, h3 {
                color: #000000 !important;
            }

            h1 {
                text-align: center;
            }

            .subtitle {
                color: #000000 !important;
                text-align: center;
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: -0.25rem;
                margin-bottom: 0.8rem;
            }

            [data-testid="stCaptionContainer"] {
                color: #000000 !important;
            }

            button[data-baseweb="tab"] {
                color: #000000 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Torneos Modena - Fotos", layout="wide")
    set_logo_background()
    set_text_colors()
    st.title("COPA DE VERANO KOMBAT " )
    st.markdown('<p class="subtitle">MODENA PADEL CENTER</p>', unsafe_allow_html=True)
    st.write("Fotos públicas organizadas por carpetas: LLAVES y ZONAS.")

    tab_zonas, tab_llaves = st.tabs(["ZONAS", "LLAVES"])

    with tab_zonas:
        render_folder("ZONAS", DRIVE_FOLDERS["ZONAS"])

    with tab_llaves:
        render_folder("LLAVES", DRIVE_FOLDERS["LLAVES"])


if __name__ == "__main__":
    main()
