# Update backend code and frontend dist
rsync -av -e ssh --exclude='__pycache__' backend qingxin:/root/
rsync -av -e ssh frontend/dist qingxin:/root/frontend