import streamlit as st
from pathlib import Path
import base64
from typing import Optional
import html
import re
import requests


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


def file_view_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"


def file_thumbnail_url(file_id: str, width: int = 1200) -> str:
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{width}"


@st.cache_data(ttl=600)
def get_folder_images(folder_id: str) -> list[dict[str, str]]:
    response = requests.get(folder_share_url(folder_id), timeout=30)
    response.raise_for_status()
    page = response.text

    image_pattern = re.compile(
        r'\[null,&quot;(?P<id>[A-Za-z0-9_-]{20,})&quot;\],null,null,null,&quot;'
        r'(?P<mime>image/(?:jpeg|jpg|png|webp|heic|heif))&quot;.*?'
        r'\[\[\[&quot;(?P<name>[^&]+?\.(?:jpg|jpeg|png|webp|heic|heif))&quot;',
        re.IGNORECASE | re.DOTALL,
    )

    images: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for match in image_pattern.finditer(page):
        file_id = match.group("id")
        if file_id in seen_ids:
            continue
        seen_ids.add(file_id)
        images.append(
            {
                "id": file_id,
                "name": html.unescape(match.group("name")),
                "mime": match.group("mime"),
            }
        )

    return images


def render_folder(name: str, folder_id: str) -> None:
    st.subheader(name)
    st.link_button(
        "Open in Google Drive",
        folder_share_url(folder_id),
        use_container_width=True,
    )

    try:
        images = get_folder_images(folder_id)
    except requests.RequestException:
        st.warning("Could not load photos right now. Please try again in a few seconds.")
        return

    if not images:
        st.info("No photos found in this folder yet.")
        return

    photo_items = "\n".join(
        (
            f'<a class="photo-link" href="{file_view_url(image["id"])}" target="_blank" '
            f'rel="noopener noreferrer">'
            f'<img src="{file_thumbnail_url(image["id"])}" alt="Photo" loading="lazy" />'
            "</a>"
        )
        for image in images
    )

    st.markdown(
        f'<div class="photo-grid">{photo_items}</div>',
        unsafe_allow_html=True,
    )


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

            div[data-testid="stTabs"] button[data-baseweb="tab"] {
                font-size: 1.05rem;
                font-weight: 700;
                min-height: 48px;
            }

            @media (max-width: 768px) {
                h1 {
                    font-size: 1.65rem !important;
                    line-height: 1.2;
                }

                .subtitle {
                    font-size: 1.1rem;
                    margin-top: 0;
                }

                .stApp {
                    background-attachment: scroll !important;
                }

                .block-container {
                    padding-top: 1rem;
                    padding-left: 0.85rem;
                    padding-right: 0.85rem;
                }

                div[data-testid="stTabs"] button[data-baseweb="tab"] {
                    font-size: 1rem;
                    min-height: 50px;
                }
            }

            .photo-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
                margin-top: 0.75rem;
            }

            .photo-link {
                display: block;
                border-radius: 0.6rem;
                overflow: hidden;
                background: rgba(255, 255, 255, 0.5);
            }

            .photo-link img {
                width: 100%;
                height: 100%;
                display: block;
                object-fit: cover;
                aspect-ratio: 1 / 1;
            }

            @media (max-width: 1024px) {
                .photo-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }

            @media (max-width: 640px) {
                .photo-grid {
                    grid-template-columns: 1fr;
                }
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
