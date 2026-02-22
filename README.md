# Torneos Modena - Streamlit Photo Webpage

This app publishes photos from your two public Google Drive folders with the same structure:

- LLAVES
- ZONAS

It also supports a venue logo at the top of the page.

## Add the venue logo

Save your logo image in this path:

assets/logomodena.jpg

If the file is present, the app displays it above the folder tabs.

## Run locally

1. Install dependencies:

	```bash
	pip install streamlit
	```

2. Start the app:

	```bash
	streamlit run main.py
	```

3. Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Publish online (Streamlit Community Cloud)

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Select this repository and set the entrypoint to:

	```
	main.py
	```

4. Deploy.

This repo already includes deployment files:

- requirements.txt
- runtime.txt
- .streamlit/config.toml

The app will show both folders (LLAVES and ZONAS) in separate tabs and render the photos directly from public Drive links.
