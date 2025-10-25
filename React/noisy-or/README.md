# Noisy OR

To run a dev server:

```bash
npm install
npm run dev
```

To build the app and deploy to the website:

```bash
npm run build
rm -rf ~/website/noisy-or/*
cp -r ./dist/* ~/website/noisy-or/
```