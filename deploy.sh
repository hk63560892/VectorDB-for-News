#!/bin/bash

# 台積電新聞檢索系統 - GitHub 上傳腳本

echo "================================================"
echo "  台積電新聞檢索系統 - GitHub 部署助手"
echo "================================================"
echo ""

# 檢查是否已經初始化 Git
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git 倉庫..."
    git init
    echo "✅ Git 倉庫初始化完成"
    echo ""
fi

# 顯示當前文件狀態
echo "📁 檢查專案文件..."
git status --short
echo ""

# 詢問 GitHub 倉庫 URL
echo "請提供你的 GitHub 倉庫 URL"
echo "格式範例: https://github.com/你的用戶名/tsmc-news-search.git"
read -p "GitHub 倉庫 URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 未提供倉庫 URL，取消上傳"
    exit 1
fi

# 檢查是否已經設定 remote
if git remote | grep -q "origin"; then
    echo "⚠️  已存在 origin remote，將更新為新的 URL"
    git remote set-url origin "$REPO_URL"
else
    echo "🔗 設定 GitHub remote..."
    git remote add origin "$REPO_URL"
fi

# 添加所有文件
echo "📦 添加文件到 Git..."
git add .

# 提交
read -p "請輸入提交訊息（直接按 Enter 使用預設訊息）: " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Initial commit: TSMC news search system with vector database"
fi

git commit -m "$COMMIT_MSG"

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "================================================"
echo "✅ 上傳完成！"
echo "================================================"
echo ""
echo "下一步："
echo "1. 訪問 https://streamlit.io/cloud"
echo "2. 用 GitHub 帳號登入"
echo "3. 點擊 'New app'"
echo "4. 選擇你的倉庫和 app.py"
echo "5. 點擊 'Deploy!'"
echo ""
echo "詳細說明請參考 DEPLOYMENT.md"
echo ""
