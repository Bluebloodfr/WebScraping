init:
	python -m venv .venv
	.venv\Scripts\activate
	python.exe -m pip install --upgrade pip
	pip install -r requirements.txt

venv:
	.venv\Scripts\activate

back:
	python back

run:
	streamlit run app.py

curl:
	wsl
	bash tourism/downlaod_zip.sh
	exit
