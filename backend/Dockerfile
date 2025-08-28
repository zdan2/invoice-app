# 1. ベースとなる「公式Pythonイメージ」をダウンロード
FROM python:3.11

# 2. 作業するフォルダを /app に指定
WORKDIR /app

# 3. 必要なライブラリを書いたファイルを先にコピー
COPY ./requirements.txt .

# 4. そのファイルを使ってライブラリをインストール
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. バックエンドの全ファイルをコンテナにコピー
COPY . .

# 6. コンテナの8000番ポートを開放
EXPOSE 8000