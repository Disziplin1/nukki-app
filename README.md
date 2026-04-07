# nukki.app — 무료 배경 제거 서비스

가입 없이, 원본 화질 그대로 배경을 제거해주는 웹앱입니다.  
rembg (U2Net 딥러닝 모델) 기반으로 동작합니다.

## 프로젝트 구조

```
nukki-app/
├── index.html        ← 프론트엔드 (정적 파일)
├── api/
│   └── remove.py     ← Vercel Python 서버리스 함수
├── requirements.txt  ← Python 의존성
├── vercel.json       ← Vercel 배포 설정
└── README.md
```

## 배포 방법

### 1. GitHub에 올리기

```bash
git init
git add .
git commit -m "init: nukki app"
git remote add origin https://github.com/YOUR_ID/nukki-app.git
git push -u origin main
```

### 2. Vercel 연결

1. [vercel.com](https://vercel.com) 접속
2. "Add New Project" → GitHub 레포 선택
3. 설정 변경 없이 바로 **Deploy** 클릭
4. 배포 완료 후 링크 공유!

## 주의사항

- Vercel 무료 플랜 기준 함수 실행 시간 최대 60초
- 첫 실행 시 rembg 모델 다운로드로 10~20초 소요될 수 있음 (이후 캐시)
- 파일 크기 제한: 20MB
- 동시 요청이 많으면 Vercel Pro 플랜 고려 (월 $20)

## 로컬 테스트

```bash
pip install -r requirements.txt
npm i -g vercel
vercel dev
```

`http://localhost:3000` 에서 확인 가능
