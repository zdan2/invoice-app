# 1. ベースとなるNode.jsイメージ
FROM node:20

# 2. 作業場所を/appに設定
WORKDIR /app

# 3. package.json関連のファイルを先にコピー
COPY package*.json ./

# 4. 依存関係をインストール
RUN npm install

# 5. プロジェクトの残りのファイルを全部コピー
COPY . .

# 6. ポートを開放
EXPOSE 3000